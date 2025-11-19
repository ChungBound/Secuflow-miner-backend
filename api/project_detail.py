from fastapi import APIRouter, Query, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import database
from ..project import Project
from ..project_history import ProjectHistory
from ..assignment_matrix_miner import AssignmentMatrixMiner
from ..changed_files_miner import ChangedFilesMiner
from ..file_dependency_matrix_miner import FileDependencyMatrixMiner
import json
import numpy as np
import pandas as pd
from pydantic import BaseModel
from typing import List, Dict, Any

router = APIRouter()

@router.get("/projects/{project_id}")
def get_project_statistics(project_id: int, db: Session = Depends(database.get_db)):
    # Fetch the main project information
    project = db.query(Project).filter(Project.id == project_id).first()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Fetch all versions (history) for the project
    project_latest_version = db.query(ProjectHistory).filter(ProjectHistory.project_id == project_id).first()
    # group: developer, security

    # Prepare the response
    project_data = {
        "project_id": project.id,
        "project_name": project.name,
        "create_time": project.created_at,
        "coordination_date": project_latest_version.timestamp,
        "ca_matrix": json.loads(project_latest_version.ca_matrix),
        "cr_matrix": json.loads(project_latest_version.cr_matrix),
        "stc_value": project_latest_version.stc_value,
        "mc_stc_value": project_latest_version.mc_stc_value,
        "dev_infos": json.loads(project_latest_version.dev_infos),
        # ignore this value
        "security_dev_emails":  []
    }

    return project_data

@router.get("/projects/{project_id}/dev_infos")
def get_project_infos(project_id: int, db: Session = Depends(database.get_db)):
    # Fetch the main project information
    project = db.query(Project).filter(Project.id == project_id).first()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Fetch all versions (history) for the project
    project_latest_version = db.query(ProjectHistory).filter(ProjectHistory.project_id == project_id).first()
    # group: developer, security

    # Prepare the response
    project_data = {
        "project_id": project.id,
        "project_name": project.name,
        "dev_infos": json.loads(project_latest_version.dev_infos),
    }

    return project_data

class DevInfoUpdate(BaseModel):
    dev_infos: List[Dict[str, Any]] # dev_infos 是一个字典类型

@router.post("/projects/{project_id}/dev_infos")
def update_dev_infos(project_id: int, dev_info_update: DevInfoUpdate, db: Session = Depends(database.get_db)):
    # Fetch the project history entry
    project_latest_version = db.query(ProjectHistory).filter(ProjectHistory.project_id == project_id).first()

    if not project_latest_version:
        raise HTTPException(status_code=404, detail="Project history not found")

    # Convert the dev_info_update data to a JSON string and store it as text
    try:
        # tutor's sample data
        # security_ids_to_find = [3, 1, 56, 76, 109, 110, 131, 136, 147, 148, 155, 201, 235, 236, 238]
        # all_user_ids = {"0":"michael@grosser.it","1":"rbayerl@zendesk.com","2":"amir.alavi@zendesk.com","3":"83986509+zendesk-mattlefevre@users.noreply.github.com","4":"anthonywoo88@gmail.com","5":"awoo@m52k6hj7hq.lan","6":"_@orien.io","7":"rajeesh.ckr@gmail.com","8":"amalcontenti-wilson@zendesk.com","9":"bgarcia@zendesk.com","10":"paul.fiorentino@zendesk.com","11":"matthew.lefevre@zendesk.com","12":"22380457+lara@users.noreply.github.com","13":"daydin@zendesk.com","14":"jyelee124@gmail.com","15":"connorbwaity@gmail.com","16":"oleg.atamanenko@gmail.com","17":"jaakjaer@zendesk.com","18":"pierce.fu@zendesk.com","19":"sathishavm@gmail.com","20":"zchitty@zendesk.com","21":"SamuelDeuter@gmail.com","22":"rsim@zendesk.com","23":"cday@zendesk.com","24":"craig-day@users.noreply.github.com","25":"yizhang@zendesk.com","26":"aleksandre.clavet@zendesk.com","27":"aglover@zendesk.com","28":"jaliu@zendesk.com","29":"tsfdye@gmail.com","30":"john@everops.com","31":"34999291+shoukoo@users.noreply.github.com","32":"shoukoo.koike@gmail.com","33":"joangeja@zendesk.com","34":"lwan@zendesk.com","35":"dtran@zendesk.com","36":"jmoter@zendesk.com","37":"adrian.bordinc@gmail.com","38":"dreuss@zendesk.com","39":"patrick.robinson@envato.com","40":"thomas.farvour@lumoslabs.com","41":"rudolphben@gmail.com","42":"cottrey@zendesk.com","43":"vadim.chernik@gmail.com","44":"jake.kelly10@gmail.com","45":"ktsanaktsidis@zendesk.com","46":"akunday@zendesk.com","47":"jswan@zendesk.com","48":"dlugo@zendesk.com","49":"alaric.calmette@gmail.com","50":"arecker@zendesk.com","51":"ashah@zendesk.com","52":"stephenoberther@gmail.com","53":"pmescalchin@zendesk.com","54":"camertron@gmail.com","55":"rygurney@zendesk.com","56":"gmathes@zendesk.com","57":"munishapc@gmail.com","58":"cng@zendesk.com","59":"stephenyusman@gmail.com","60":"cthilgen@zendesk.com","61":"igorsharshun@gmail.com","62":"tranhaidangtn10609@gmail.com","63":"lfriedman@zendesk.com","64":"dragonfax@gmail.com","65":"mklitte@zendesk.com","66":"plonergan@zendesk.com","67":"adman.com@gmail.com","68":"dani.hodovic@gmail.com","69":"peter@magnetikonline.com","70":"thilgen@users.noreply.github.com","71":"ryan.a.gurney@gmail.com","72":"jonathon.bel.melbourne@gmail.com","73":"bcolfer@zendesk.com","74":"rodrigo@sdfg.com.ar","75":"pe@speedledger.se","76":"gcahill@zendesk.com","77":"support@dependabot.com","78":"dasch@zendesk.com","79":"iao@iki.fi","80":"daniel.schierbeck@gmail.com","81":"ghammadi@gmail.com","82":"kjtsanaktsidis@gmail.com","83":"neerfri@gmail.com","84":"russell.sim@gmail.com","85":"jonmoter@gmail.com","86":"elaine.ocarroll@gmail.com","87":"greysteil@gmail.com","88":"th9382@gmail.com","89":"ywu@zendesk.com","90":"hgokavarapu@zendesk.com","91":"raittes@gmail.com","92":"s.sidorchick@gmail.com","93":"tanle.oz@gmail.com","94":"adamb3189@gmail.com","95":"stan.pitucha@envato.com","96":"david@singularities.org","97":"dallen@zendesk.com","98":"steen.lehmann@gmail.com","99":"zachwr@zillowgroup.com","100":"zacharygwright@gmail.com","101":"jesse.goerz@plansource.com","102":"lcorreadecarvalhojr@zendesk.com","103":"indika@zendesk.com","104":"mpchadwick@gmail.com","105":"anthony@contentful.com","106":"hyperair@debian.org","107":"glecerf@lafourchette.com","108":"dndungu@users.noreply.github.com","109":"epak@zendesk.com","110":"erichyp@gmail.com","111":"krzysztof.wawer@gmail.com","112":"tmcinerney@zendesk.com","113":"travers@mcinerney.me","114":"lcannici@zendesk.com","115":"hhsu@zendesk.com","116":"tngo@zendesk.com","117":"mhuston@zendesk.com","118":"henrikj@me.com","119":"cgwippern@gmail.com","120":"ibrahim.awwal@gmail.com","121":"nfreeland@zendesk.com","122":"rsandler@zendesk.com","123":"jbarreneche@restorando.com","124":"ahart@zendesk.com","125":"tamgrosser@gmail.com","126":"tcohen@zendesk.com","127":"irwaters@gmail.com","128":"nchadha@zendesk.com","129":"upcomingnewton@gmail.com","130":"mario@mariovisic.com","131":"jason@suarez.email","132":"pschambacher@zendesk.com","133":"mick@staugaard.com","134":"neroleung@gmail.com","135":"ducksteven@gmail.com","136":"mariozaizar@gmail.com","137":"bquorning@users.noreply.github.com","138":"jstillwell@zendesk.com","139":"benjamin@quorning.net","140":"apanzer@zendesk.com","141":"aevans@zendesk.com","142":"evade@hyperevade.net","143":"rikeoka@gmail.com","144":"rikeoka@zendesk.com","145":"albert@dixon.rocks","146":"iwaters@zendesk.com","147":"anthony.github@asellitt.com","148":"mmukhtarov@zendesk.com","149":"edenisn@gmail.com","150":"livathinos.spyros@gmail.com","151":"calcavecchia@gmail.com","152":"ncalcavecchia@zendesk.com","153":"andreionut@gmail.com","154":"abalcanasu@zendesk.com","155":"bstraub@zendesk.com","156":"ben@straub.cc","157":"dribeiro@zendesk.com","158":"gorodetsky@gmail.com","159":"figocia@gmail.com","160":"yufei.chen@redbubble.com","161":"lucas.wilsonrichter@redbubble.com","162":"andrew@andrewjones.id.au","163":"zliu@zendesk.com","164":"rata@users.noreply.github.com","165":"s-onishi@dts.co.jp","166":"michael.bouvy@gmail.com","167":"fneves@zendesk.com","168":"mblaschke82@gmail.com","169":"olaf+github@zendesk.com","170":"ocke@users.noreply.github.com","171":"steven.davidovitz@gmail.com","172":"sdavidovitz@zendesk.com","173":"henders@users.noreply.github.com","174":"henders@gmail.com","175":"wyau@zendesk.com","176":"kintner@gmail.com","177":"ckintner@zendesk.com","178":"mwerner@zendesk.com","179":"mwerner@users.noreply.github.com","180":"perhuman@gmail.com","181":"msufa@users.noreply.github.com","182":"msufa@zendesk.com","183":"jason@denizac.org","184":"jden@zendesk.com","185":"dean@deanperry.net","186":"sbrnunes@gmail.com","187":"snunes@zendesk.com","188":"o.laurendeau@gmail.com","189":"jacob.bednarz@gmail.com","190":"cmckni3@gmail.com","191":"m@mjw.io","192":"akash@akash.im","193":"jeoffrey.bauvin.ext@boursorama.fr","194":"mauro.codella@gmail.com","195":"jacob@jacobatzen.dk","196":"sj26@sj26.com","197":"jatzen@gmail.com","198":"lbrfalcao@gmail.com","199":"ang.yi.hong@gmail.com","200":"amartinez@zendesk.com","201":"duduribeiro.gba@gmail.com","202":"vinh@listia.com","203":"jesper@zendesk.com","204":"jsmale@zendesk.com","205":"sungju@softwaregeeks.org","206":"gabe@zendesk.com","207":"kurei@axcoto.com","208":"hsiojo@zendesk.com","209":"rdhanoa@zendesk.com","210":"giancarlo.salamanca@envato.com","211":"shender@zendesk.com","212":"zendesk-shender@users.noreply.github.com","213":"glen.stampoultzis@envato.com","214":"chenpaul914@gmail.com","215":"pchen@zendesk.com","216":"igor@zendesk.com","217":"grosser.michael@gmail.com","218":"apanzerj@users.noreply.github.com","219":"romansandler0@gmail.com","220":"jmoter@6661-jmoter.local","221":"sgray@zendesk.com","222":"apanzerj@gmail.com","223":"stubotnik@users.noreply.github.com","224":"pswadi@zendesk.com","225":"pitr.vern@gmail.com","226":"carcher@zendesk.com","227":"jcheatham@zendesk.com","228":"jcheatham@users.noreply.github.com","229":"pobrien@zendesk.com","230":"ben@zendesk.com","231":"ben@gimbo.net","232":"tim@buchwaldt.ws","233":"me@iroller.ru","234":"voanhduy1512@live.com","235":"jish@users.noreply.github.com","236":"josh.lubaway@gmail.com","237":"josh@zendesk.com","238":"tony@inlight.com.au","239":"wtfiwtz@gmail.com"}
        # formatted_list = [
        #     {"email": email, "isSecurity": int(user_id) in security_ids_to_find}
        #     for user_id, email in all_user_ids.items()
        # ]
        # [{"email": "michael@grosser.it", "isSecurity": false}, {"email": "rbayerl@zendesk.com", "isSecurity": true}, {"email": "amir.alavi@zendesk.com", "isSecurity": false}, {"email": "83986509+zendesk-mattlefevre@users.noreply.github.com", "isSecurity": true}, {"email": "anthonywoo88@gmail.com", "isSecurity": false}, {"email": "awoo@m52k6hj7hq.lan", "isSecurity": false}, {"email": "_@orien.io", "isSecurity": false}, {"email": "rajeesh.ckr@gmail.com", "isSecurity": false}, {"email": "amalcontenti-wilson@zendesk.com", "isSecurity": false}, {"email": "bgarcia@zendesk.com", "isSecurity": false}, {"email": "paul.fiorentino@zendesk.com", "isSecurity": false}, {"email": "matthew.lefevre@zendesk.com", "isSecurity": false}, {"email": "22380457+lara@users.noreply.github.com", "isSecurity": false}, {"email": "daydin@zendesk.com", "isSecurity": false}, {"email": "jyelee124@gmail.com", "isSecurity": false}, {"email": "connorbwaity@gmail.com", "isSecurity": false}, {"email": "oleg.atamanenko@gmail.com", "isSecurity": false}, {"email": "jaakjaer@zendesk.com", "isSecurity": false}, {"email": "pierce.fu@zendesk.com", "isSecurity": false}, {"email": "sathishavm@gmail.com", "isSecurity": false}, {"email": "zchitty@zendesk.com", "isSecurity": false}, {"email": "SamuelDeuter@gmail.com", "isSecurity": false}, {"email": "rsim@zendesk.com", "isSecurity": false}, {"email": "cday@zendesk.com", "isSecurity": false}, {"email": "craig-day@users.noreply.github.com", "isSecurity": false}, {"email": "yizhang@zendesk.com", "isSecurity": false}, {"email": "aleksandre.clavet@zendesk.com", "isSecurity": false}, {"email": "aglover@zendesk.com", "isSecurity": false}, {"email": "jaliu@zendesk.com", "isSecurity": false}, {"email": "tsfdye@gmail.com", "isSecurity": false}, {"email": "john@everops.com", "isSecurity": false}, {"email": "34999291+shoukoo@users.noreply.github.com", "isSecurity": false}, {"email": "shoukoo.koike@gmail.com", "isSecurity": false}, {"email": "joangeja@zendesk.com", "isSecurity": false}, {"email": "lwan@zendesk.com", "isSecurity": false}, {"email": "dtran@zendesk.com", "isSecurity": false}, {"email": "jmoter@zendesk.com", "isSecurity": false}, {"email": "adrian.bordinc@gmail.com", "isSecurity": false}, {"email": "dreuss@zendesk.com", "isSecurity": false}, {"email": "patrick.robinson@envato.com", "isSecurity": false}, {"email": "thomas.farvour@lumoslabs.com", "isSecurity": false}, {"email": "rudolphben@gmail.com", "isSecurity": false}, {"email": "cottrey@zendesk.com", "isSecurity": false}, {"email": "vadim.chernik@gmail.com", "isSecurity": false}, {"email": "jake.kelly10@gmail.com", "isSecurity": false}, {"email": "ktsanaktsidis@zendesk.com", "isSecurity": false}, {"email": "akunday@zendesk.com", "isSecurity": false}, {"email": "jswan@zendesk.com", "isSecurity": false}, {"email": "dlugo@zendesk.com", "isSecurity": false}, {"email": "alaric.calmette@gmail.com", "isSecurity": false}, {"email": "arecker@zendesk.com", "isSecurity": false}, {"email": "ashah@zendesk.com", "isSecurity": false}, {"email": "stephenoberther@gmail.com", "isSecurity": false}, {"email": "pmescalchin@zendesk.com", "isSecurity": false}, {"email": "camertron@gmail.com", "isSecurity": false}, {"email": "rygurney@zendesk.com", "isSecurity": false}, {"email": "gmathes@zendesk.com", "isSecurity": true}, {"email": "munishapc@gmail.com", "isSecurity": false}, {"email": "cng@zendesk.com", "isSecurity": false}, {"email": "stephenyusman@gmail.com", "isSecurity": false}, {"email": "cthilgen@zendesk.com", "isSecurity": false}, {"email": "igorsharshun@gmail.com", "isSecurity": false}, {"email": "tranhaidangtn10609@gmail.com", "isSecurity": false}, {"email": "lfriedman@zendesk.com", "isSecurity": false}, {"email": "dragonfax@gmail.com", "isSecurity": false}, {"email": "mklitte@zendesk.com", "isSecurity": false}, {"email": "plonergan@zendesk.com", "isSecurity": false}, {"email": "adman.com@gmail.com", "isSecurity": false}, {"email": "dani.hodovic@gmail.com", "isSecurity": false}, {"email": "peter@magnetikonline.com", "isSecurity": false}, {"email": "thilgen@users.noreply.github.com", "isSecurity": false}, {"email": "ryan.a.gurney@gmail.com", "isSecurity": false}, {"email": "jonathon.bel.melbourne@gmail.com", "isSecurity": false}, {"email": "bcolfer@zendesk.com", "isSecurity": false}, {"email": "rodrigo@sdfg.com.ar", "isSecurity": false}, {"email": "pe@speedledger.se", "isSecurity": false}, {"email": "gcahill@zendesk.com", "isSecurity": true}, {"email": "support@dependabot.com", "isSecurity": false}, {"email": "dasch@zendesk.com", "isSecurity": false}, {"email": "iao@iki.fi", "isSecurity": false}, {"email": "daniel.schierbeck@gmail.com", "isSecurity": false}, {"email": "ghammadi@gmail.com", "isSecurity": false}, {"email": "kjtsanaktsidis@gmail.com", "isSecurity": false}, {"email": "neerfri@gmail.com", "isSecurity": false}, {"email": "russell.sim@gmail.com", "isSecurity": false}, {"email": "jonmoter@gmail.com", "isSecurity": false}, {"email": "elaine.ocarroll@gmail.com", "isSecurity": false}, {"email": "greysteil@gmail.com", "isSecurity": false}, {"email": "th9382@gmail.com", "isSecurity": false}, {"email": "ywu@zendesk.com", "isSecurity": false}, {"email": "hgokavarapu@zendesk.com", "isSecurity": false}, {"email": "raittes@gmail.com", "isSecurity": false}, {"email": "s.sidorchick@gmail.com", "isSecurity": false}, {"email": "tanle.oz@gmail.com", "isSecurity": false}, {"email": "adamb3189@gmail.com", "isSecurity": false}, {"email": "stan.pitucha@envato.com", "isSecurity": false}, {"email": "david@singularities.org", "isSecurity": false}, {"email": "dallen@zendesk.com", "isSecurity": false}, {"email": "steen.lehmann@gmail.com", "isSecurity": false}, {"email": "zachwr@zillowgroup.com", "isSecurity": false}, {"email": "zacharygwright@gmail.com", "isSecurity": false}, {"email": "jesse.goerz@plansource.com", "isSecurity": false}, {"email": "lcorreadecarvalhojr@zendesk.com", "isSecurity": false}, {"email": "indika@zendesk.com", "isSecurity": false}, {"email": "mpchadwick@gmail.com", "isSecurity": false}, {"email": "anthony@contentful.com", "isSecurity": false}, {"email": "hyperair@debian.org", "isSecurity": false}, {"email": "glecerf@lafourchette.com", "isSecurity": false}, {"email": "dndungu@users.noreply.github.com", "isSecurity": false}, {"email": "epak@zendesk.com", "isSecurity": true}, {"email": "erichyp@gmail.com", "isSecurity": true}, {"email": "krzysztof.wawer@gmail.com", "isSecurity": false}, {"email": "tmcinerney@zendesk.com", "isSecurity": false}, {"email": "travers@mcinerney.me", "isSecurity": false}, {"email": "lcannici@zendesk.com", "isSecurity": false}, {"email": "hhsu@zendesk.com", "isSecurity": false}, {"email": "tngo@zendesk.com", "isSecurity": false}, {"email": "mhuston@zendesk.com", "isSecurity": false}, {"email": "henrikj@me.com", "isSecurity": false}, {"email": "cgwippern@gmail.com", "isSecurity": false}, {"email": "ibrahim.awwal@gmail.com", "isSecurity": false}, {"email": "nfreeland@zendesk.com", "isSecurity": false}, {"email": "rsandler@zendesk.com", "isSecurity": false}, {"email": "jbarreneche@restorando.com", "isSecurity": false}, {"email": "ahart@zendesk.com", "isSecurity": false}, {"email": "tamgrosser@gmail.com", "isSecurity": false}, {"email": "tcohen@zendesk.com", "isSecurity": false}, {"email": "irwaters@gmail.com", "isSecurity": false}, {"email": "nchadha@zendesk.com", "isSecurity": false}, {"email": "upcomingnewton@gmail.com", "isSecurity": false}, {"email": "mario@mariovisic.com", "isSecurity": false}, {"email": "jason@suarez.email", "isSecurity": true}, {"email": "pschambacher@zendesk.com", "isSecurity": false}, {"email": "mick@staugaard.com", "isSecurity": false}, {"email": "neroleung@gmail.com", "isSecurity": false}, {"email": "ducksteven@gmail.com", "isSecurity": false}, {"email": "mariozaizar@gmail.com", "isSecurity": true}, {"email": "bquorning@users.noreply.github.com", "isSecurity": false}, {"email": "jstillwell@zendesk.com", "isSecurity": false}, {"email": "benjamin@quorning.net", "isSecurity": false}, {"email": "apanzer@zendesk.com", "isSecurity": false}, {"email": "aevans@zendesk.com", "isSecurity": false}, {"email": "evade@hyperevade.net", "isSecurity": false}, {"email": "rikeoka@gmail.com", "isSecurity": false}, {"email": "rikeoka@zendesk.com", "isSecurity": false}, {"email": "albert@dixon.rocks", "isSecurity": false}, {"email": "iwaters@zendesk.com", "isSecurity": false}, {"email": "anthony.github@asellitt.com", "isSecurity": true}, {"email": "mmukhtarov@zendesk.com", "isSecurity": true}, {"email": "edenisn@gmail.com", "isSecurity": false}, {"email": "livathinos.spyros@gmail.com", "isSecurity": false}, {"email": "calcavecchia@gmail.com", "isSecurity": false}, {"email": "ncalcavecchia@zendesk.com", "isSecurity": false}, {"email": "andreionut@gmail.com", "isSecurity": false}, {"email": "abalcanasu@zendesk.com", "isSecurity": false}, {"email": "bstraub@zendesk.com", "isSecurity": true}, {"email": "ben@straub.cc", "isSecurity": false}, {"email": "dribeiro@zendesk.com", "isSecurity": false}, {"email": "gorodetsky@gmail.com", "isSecurity": false}, {"email": "figocia@gmail.com", "isSecurity": false}, {"email": "yufei.chen@redbubble.com", "isSecurity": false}, {"email": "lucas.wilsonrichter@redbubble.com", "isSecurity": false}, {"email": "andrew@andrewjones.id.au", "isSecurity": false}, {"email": "zliu@zendesk.com", "isSecurity": false}, {"email": "rata@users.noreply.github.com", "isSecurity": false}, {"email": "s-onishi@dts.co.jp", "isSecurity": false}, {"email": "michael.bouvy@gmail.com", "isSecurity": false}, {"email": "fneves@zendesk.com", "isSecurity": false}, {"email": "mblaschke82@gmail.com", "isSecurity": false}, {"email": "olaf+github@zendesk.com", "isSecurity": false}, {"email": "ocke@users.noreply.github.com", "isSecurity": false}, {"email": "steven.davidovitz@gmail.com", "isSecurity": false}, {"email": "sdavidovitz@zendesk.com", "isSecurity": false}, {"email": "henders@users.noreply.github.com", "isSecurity": false}, {"email": "henders@gmail.com", "isSecurity": false}, {"email": "wyau@zendesk.com", "isSecurity": false}, {"email": "kintner@gmail.com", "isSecurity": false}, {"email": "ckintner@zendesk.com", "isSecurity": false}, {"email": "mwerner@zendesk.com", "isSecurity": false}, {"email": "mwerner@users.noreply.github.com", "isSecurity": false}, {"email": "perhuman@gmail.com", "isSecurity": false}, {"email": "msufa@users.noreply.github.com", "isSecurity": false}, {"email": "msufa@zendesk.com", "isSecurity": false}, {"email": "jason@denizac.org", "isSecurity": false}, {"email": "jden@zendesk.com", "isSecurity": false}, {"email": "dean@deanperry.net", "isSecurity": false}, {"email": "sbrnunes@gmail.com", "isSecurity": false}, {"email": "snunes@zendesk.com", "isSecurity": false}, {"email": "o.laurendeau@gmail.com", "isSecurity": false}, {"email": "jacob.bednarz@gmail.com", "isSecurity": false}, {"email": "cmckni3@gmail.com", "isSecurity": false}, {"email": "m@mjw.io", "isSecurity": false}, {"email": "akash@akash.im", "isSecurity": false}, {"email": "jeoffrey.bauvin.ext@boursorama.fr", "isSecurity": false}, {"email": "mauro.codella@gmail.com", "isSecurity": false}, {"email": "jacob@jacobatzen.dk", "isSecurity": false}, {"email": "sj26@sj26.com", "isSecurity": false}, {"email": "jatzen@gmail.com", "isSecurity": false}, {"email": "lbrfalcao@gmail.com", "isSecurity": false}, {"email": "ang.yi.hong@gmail.com", "isSecurity": false}, {"email": "amartinez@zendesk.com", "isSecurity": false}, {"email": "duduribeiro.gba@gmail.com", "isSecurity": true}, {"email": "vinh@listia.com", "isSecurity": false}, {"email": "jesper@zendesk.com", "isSecurity": false}, {"email": "jsmale@zendesk.com", "isSecurity": false}, {"email": "sungju@softwaregeeks.org", "isSecurity": false}, {"email": "gabe@zendesk.com", "isSecurity": false}, {"email": "kurei@axcoto.com", "isSecurity": false}, {"email": "hsiojo@zendesk.com", "isSecurity": false}, {"email": "rdhanoa@zendesk.com", "isSecurity": false}, {"email": "giancarlo.salamanca@envato.com", "isSecurity": false}, {"email": "shender@zendesk.com", "isSecurity": false}, {"email": "zendesk-shender@users.noreply.github.com", "isSecurity": false}, {"email": "glen.stampoultzis@envato.com", "isSecurity": false}, {"email": "chenpaul914@gmail.com", "isSecurity": false}, {"email": "pchen@zendesk.com", "isSecurity": false}, {"email": "igor@zendesk.com", "isSecurity": false}, {"email": "grosser.michael@gmail.com", "isSecurity": false}, {"email": "apanzerj@users.noreply.github.com", "isSecurity": false}, {"email": "romansandler0@gmail.com", "isSecurity": false}, {"email": "jmoter@6661-jmoter.local", "isSecurity": false}, {"email": "sgray@zendesk.com", "isSecurity": false}, {"email": "apanzerj@gmail.com", "isSecurity": false}, {"email": "stubotnik@users.noreply.github.com", "isSecurity": false}, {"email": "pswadi@zendesk.com", "isSecurity": false}, {"email": "pitr.vern@gmail.com", "isSecurity": false}, {"email": "carcher@zendesk.com", "isSecurity": false}, {"email": "jcheatham@zendesk.com", "isSecurity": false}, {"email": "jcheatham@users.noreply.github.com", "isSecurity": false}, {"email": "pobrien@zendesk.com", "isSecurity": false}, {"email": "ben@zendesk.com", "isSecurity": false}, {"email": "ben@gimbo.net", "isSecurity": false}, {"email": "tim@buchwaldt.ws", "isSecurity": false}, {"email": "me@iroller.ru", "isSecurity": false}, {"email": "voanhduy1512@live.com", "isSecurity": false}, {"email": "jish@users.noreply.github.com", "isSecurity": true}, {"email": "josh.lubaway@gmail.com", "isSecurity": true}, {"email": "josh@zendesk.com", "isSecurity": false}, {"email": "tony@inlight.com.au", "isSecurity": true}, {"email": "wtfiwtz@gmail.com", "isSecurity": false}]
        security_devs = [info['email'] for info in dev_info_update.dev_infos if info['isSecurity']]
        
        CR = pd.DataFrame(json.loads(project_latest_version.cr_matrix))
        CA = pd.DataFrame(json.loads(project_latest_version.ca_matrix))

        all_devs = CR.index.tolist() 

        security_devs_indices = [user for user in all_devs if user in security_devs]
        normal_devs_indices = [user for user in all_devs if user not in security_devs]
        
        def mc_diff(mc_cr_df, mc_ca_df, devs, security_devs):
            diff_count = 0
            for dev in devs:
                for sec_dev in security_devs:
                    if mc_cr_df.loc[dev, sec_dev] > 0 and mc_ca_df.loc[dev, sec_dev] > 0:
                        diff_count += 1
                    if mc_cr_df.loc[sec_dev, dev] > 0 and mc_ca_df.loc[sec_dev, dev] > 0:
                        diff_count += 1
            return diff_count

        def mc_cr_total(mc_cr_df, devs, security_devs):
            total_count = 0
            for dev in devs:
                for sec_dev in security_devs:
                    if mc_cr_df.loc[dev, sec_dev] > 0:
                        total_count += 1
                    if mc_cr_df.loc[sec_dev, dev] > 0:
                        total_count += 1
            return total_count

        def mc_stc(mc_cr_df, mc_ca_df, devs, security_devs):
            diff = mc_diff(mc_cr_df, mc_ca_df, devs, security_devs)
            total = mc_cr_total(mc_cr_df, devs, security_devs)
            if total == 0:
                return 0
            return diff / total

        mc_stc_score = mc_stc(CR, CA, normal_devs_indices, security_devs_indices)
        print('MC-STC Score: ', mc_stc_score)

        project_latest_version.mc_stc_value = mc_stc_score
        project_latest_version.dev_infos = json.dumps(dev_info_update.dev_infos)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error updating dev_infos: {str(e)}")

    return {"message": "dev_infos updated successfully"}
