import os
import json
import datetime
import subprocess
import argparse
import pandas as pd
import random
import string

from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Float, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

# SQLAlchemy base setup
Base = declarative_base()

# SQLAlchemy Models

class Project(Base):
    __tablename__ = 'project'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    # Relationship to ProjectHistory
    histories = relationship('ProjectHistory', back_populates='project')


class ProjectHistory(Base):
    __tablename__ = 'project_history'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(Integer, ForeignKey('project.id'))
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    
    # Result fields (moved from ProjectResults)
    ca_matrix = Column(Text)  # CA matrix in JSON format
    cr_matrix = Column(Text)  # CR matrix in JSON format
    stc_value = Column(Float)  # STC value
    mc_stc_value = Column(Float)  # MC-STC value
    security_dev_emails = Column(Text, nullable=True) 
    dev_infos = Column(Text, nullable=True)  # dev_infos

    # Relationship back to Project
    project = relationship('Project', back_populates='histories')

    # Relationships to miners
    assignment_matrix_miner = relationship('AssignmentMatrixMiner', back_populates='history')
    changed_files_miner = relationship('ChangedFilesMiner', back_populates='history')
    file_dependency_matrix_miner = relationship('FileDependencyMatrixMiner', back_populates='history')

class AssignmentMatrixMiner(Base):
    __tablename__ = 'assignment_matrix_miner'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    history_id = Column(Integer, ForeignKey('project_history.id'))  # Link to ProjectHistory
    id_to_file = Column(Text, nullable=False)
    assignment_matrix = Column(Text, nullable=False)
    id_to_user = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    history = relationship('ProjectHistory', back_populates='assignment_matrix_miner')


class ChangedFilesMiner(Base):
    __tablename__ = 'changed_files_miner'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    history_id = Column(Integer, ForeignKey('project_history.id'))  # Link to ProjectHistory
    id_to_file = Column(Text, nullable=False)
    id_to_user = Column(Text, nullable=False)
    changed_files_by_user = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    history = relationship('ProjectHistory', back_populates='changed_files_miner')


class FileDependencyMatrixMiner(Base):
    __tablename__ = 'file_dependency_matrix_miner'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    history_id = Column(Integer, ForeignKey('project_history.id'))  # Link to ProjectHistory
    id_to_file = Column(Text, nullable=False)
    file_dependency_matrix = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    history = relationship('ProjectHistory', back_populates='file_dependency_matrix_miner')

# Function to load JSON data
def load_json(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

def calculate_stc(CR, CA):
    satisfied_requirements = ((CR > 0) & (CA > 0)).sum().sum()  # Sum of True values
    total_requirements = (CR > 0).sum().sum()  # Sum of all True values in CR
    return satisfied_requirements / total_requirements if total_requirements > 0 else 0

# Function to load miner data and calculate results
def load_miner_data(directory_path, project_name, timestamp, db_url='sqlite:///miner_data.db'):
    # Set up the database engine and session
    engine = create_engine(db_url)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    # Create or find the project
    project = session.query(Project).filter(Project.name == project_name).first()
    if not project:
        project = Project(name=project_name)
        session.add(project)
        session.commit()

    # Create a new project history with the provided timestamp
    project_history = ProjectHistory(
        project_id=project.id,
        timestamp=timestamp
    )
    session.add(project_history)
    session.commit()

    # Paths to miner directories
    assignment_matrix_miner_path = os.path.join(directory_path, 'AssignmentMatrixMiner')
    changed_files_miner_path = os.path.join(directory_path, 'ChangedFilesMiner')
    file_dependency_matrix_miner_path = os.path.join(directory_path, 'FileDependencyMatrixMiner')

    # Load and store AssignmentMatrixMiner data
    assignment_matrix_miner = AssignmentMatrixMiner(
        history_id=project_history.id,
        id_to_file=json.dumps(load_json(os.path.join(assignment_matrix_miner_path, 'idToFile.json'))),
        assignment_matrix=json.dumps(load_json(os.path.join(assignment_matrix_miner_path, 'AssignmentMatrix.json'))),
        id_to_user=json.dumps(load_json(os.path.join(assignment_matrix_miner_path, 'idToUser.json')))
    )
    session.add(assignment_matrix_miner)

    # Load and store ChangedFilesMiner data
    changed_files_miner = ChangedFilesMiner(
        history_id=project_history.id,
        id_to_file=json.dumps(load_json(os.path.join(changed_files_miner_path, 'idToFile.json'))),
        id_to_user=json.dumps(load_json(os.path.join(changed_files_miner_path, 'idToUser.json'))),
        changed_files_by_user=json.dumps(load_json(os.path.join(changed_files_miner_path, 'ChangedFilesByUser.json')))
    )
    session.add(changed_files_miner)

    # Load and store FileDependencyMatrixMiner data
    file_dependency_matrix_miner = FileDependencyMatrixMiner(
        history_id=project_history.id,
        id_to_file=json.dumps(load_json(os.path.join(file_dependency_matrix_miner_path, 'idToFile.json'))),
        file_dependency_matrix=json.dumps(load_json(os.path.join(file_dependency_matrix_miner_path, 'FileDependencyMatrix.json')))
    )
    session.add(file_dependency_matrix_miner)

    # Calculate CR Matrix
    assignment_matrix_data = load_json(os.path.join(assignment_matrix_miner_path, 'AssignmentMatrix.json'))
    assignment_id_to_file = load_json(os.path.join(assignment_matrix_miner_path, 'idToFile.json'))
    assignment_id_to_user = load_json(os.path.join(assignment_matrix_miner_path, 'idToUser.json'))
    # Convert the JSON data into a DataFrame
    assignment_matrix_df = pd.DataFrame(assignment_matrix_data).fillna(0).astype(int)

    # Map IDs to file names and user emails
    assignment_matrix_df.index = assignment_matrix_df.index.map(assignment_id_to_file)
    assignment_matrix_df.columns = assignment_matrix_df.columns.map(assignment_id_to_user)

    assignment_matrix_df = assignment_matrix_df.transpose()

    dependency_id_to_file = load_json(os.path.join(file_dependency_matrix_miner_path, 'idToFile.json'))
    dependency_matrix = load_json(os.path.join(file_dependency_matrix_miner_path, 'FileDependencyMatrix.json'))

    file_names = [dependency_id_to_file[str(i)] for i in range(len(dependency_id_to_file))]
    dependency_matrix_df = pd.DataFrame(0, index=file_names, columns=file_names)

    # Populate the DataFrame with the dependency data
    for file_id, dependencies in dependency_matrix.items():
        file_name = dependency_id_to_file[file_id]
        for dep_id, count in dependencies.items():
            dep_name = dependency_id_to_file[dep_id]
            dependency_matrix_df.loc[file_name, dep_name] = count
    
    TA_TD = assignment_matrix_df.dot(dependency_matrix_df)

    CR = TA_TD.dot(assignment_matrix_df.transpose())

    # Calculate CA Matrix
    assignment_matrix_data = load_json(os.path.join(assignment_matrix_miner_path, 'AssignmentMatrix.json'))
    changed_files_id_to_file = load_json(os.path.join(changed_files_miner_path, 'idToFile.json'))
    changed_files_id_to_user = load_json(os.path.join(changed_files_miner_path, 'idToUser.json'))
    changed_files_matrix = load_json(os.path.join(changed_files_miner_path, 'ChangedFilesByUser.json'))
    
    # Create mappings for user IDs to emails and file IDs to file names
    changed_files_user_email_map = {int(k): v for k, v in changed_files_id_to_user.items()}
    changed_files_file_name_map = {int(k): v for k, v in changed_files_id_to_file.items()}

    # Prepare the data for the DataFrame
    changed_files_data = {}
    for user_id, file_ids in changed_files_matrix.items():
        user_email = changed_files_user_email_map[int(user_id)]
        file_changes = {}
        for file_id in file_ids:
            file_name = changed_files_file_name_map[int(file_id)]
            file_changes[file_name] = file_changes.get(file_name, 0) + 1
        changed_files_data[user_email] = file_changes

    # Create a DataFrame
    changed_files_df = pd.DataFrame(changed_files_data).fillna(0).astype(int)

    # Transpose to match the required structure (user emails as rows, file names as columns)
    changed_files_df = changed_files_df.T

    user_emails = changed_files_df.index
    CA = pd.DataFrame(0, index=user_emails, columns=user_emails)

    # Calculate the coordination activity (CA) matrix
    for file_name in changed_files_df.columns:
        # Get the users who have edited this file
        editors = changed_files_df[file_name][changed_files_df[file_name] > 0]
        # Update the CA matrix for each pair of users who edited the same file
        for i, user_i in enumerate(editors.index):
            for j, user_j in enumerate(editors.index):
                if i != j:
                    CA.at[user_i, user_j] += 1

    def calculate_stc(CR, CA):
        satisfied_requirements = ((CR > 0) & (CA > 0)).sum().sum()  # Sum of True values
        total_requirements = (CR > 0).sum().sum()  # Sum of all True values in CR
        return satisfied_requirements / total_requirements if total_requirements > 0 else 0

    dev_infos = [{"email": email, "isSecurity": False} for email in user_emails]

    # Store results in ProjectHistory
    project_history.ca_matrix = CA.to_json()
    project_history.cr_matrix = CR.to_json()
    project_history.stc_value = calculate_stc(CR, CA)
    project_history.dev_infos = json.dumps(dev_infos)
    project_history.security_dev_emails = json.dumps([])
    
    session.commit()

    print(f"Data loaded and results calculated for project: {project_name} at {timestamp}")

    create_dummy_projects(session, 20, CA.to_json(), CR.to_json(), json.dumps(dev_infos))

def generate_random_project_name(length=8):
    return 'dummy_project_' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

def generate_random_value(min_value=0, max_value=1):
    return round(random.uniform(min_value, max_value), 4)

def create_dummy_projects(session, num_projects, ca, cr, dev_infos):
    for _ in range(num_projects):
        project_name = generate_random_project_name()
        project = Project(name=project_name)
        session.add(project)
        session.commit()

        project_history = ProjectHistory(
            project_id=project.id,
            stc_value=generate_random_value(),
            mc_stc_value=generate_random_value(),
            ca_matrix=ca,
            cr_matrix=cr,
            dev_infos=dev_infos
        )
        session.add(project_history)
        session.commit()

        print(f"Created project {project_name} with STC {project_history.stc_value} and MC-STC {project_history.mc_stc_value}")

# Main function to handle command-line execution
def main():
    parser = argparse.ArgumentParser(description='Process miner data and calculate results.')
    parser.add_argument('directory_path', type=str, help='Path to the miner data directory')
    parser.add_argument('project_name', type=str, help='Name of the project')
    parser.add_argument('project_branch', type=str, help='Branch of this project')
    parser.add_argument('--timestamp', type=lambda s: datetime.datetime.strptime(s, '%Y-%m-%d %H:%M:%S'),
                        default=datetime.datetime.utcnow(), help='Timestamp for project history (format: "YYYY-MM-DD HH:MM:SS")')
    parser.add_argument('--db_url', type=str, default='sqlite:///miner_data.db', help='Database URL (default: sqlite:///miner_data.db)')

    args = parser.parse_args()
    current_script_dir = os.path.dirname(os.path.abspath(__file__))

    commands = [
        'FileDependencyMatrixMiner',
        'AssignmentMatrixMiner',
        'ChangedFilesMiner'
    ]
    
    for miner in commands:
        command = [
            'java', '-jar', current_script_dir + '/tnm-cli.jar',
            miner,
            '--repository', args.directory_path, args.project_branch
        ]
        
        print(f"Running command: {' '.join(command)}")
        result = subprocess.run(command, capture_output=True, text=True)
        
        print("Standard Output:", result.stdout)
        print("Error Output:", result.stderr)
        print("Return Code:", result.returncode)
        
        if result.returncode != 0:
            print(f"Error running command: {miner[0]}")
            break
    
    load_miner_data(current_script_dir + '/result', args.project_name, args.timestamp, args.db_url)

if __name__ == '__main__':
    main()