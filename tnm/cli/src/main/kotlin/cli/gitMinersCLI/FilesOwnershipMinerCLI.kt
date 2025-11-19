package cli.gitMinersCLI

import cli.gitMinersCLI.base.GitMinerMultithreadedOneBranchCLI
import dataProcessor.FilesOwnershipDataProcessor
import miners.gitMiners.FilesOwnershipMiner
import org.eclipse.jgit.internal.storage.file.FileRepository
import util.HelpFunctionsUtil
import java.io.File

class FilesOwnershipMinerCLI : GitMinerMultithreadedOneBranchCLI(
    "FilesOwnershipMiner",
    "Miner yields following JSON files. $HELP_DEVELOPER_KNOWLEDGE. $HELP_FILES_OWNERSHIP. $HELP_POTENTIAL_OWNERSHIP"
) {

    companion object {
        const val HELP_DEVELOPER_KNOWLEDGE = "JSON file with map of maps, where the outer " +
                "key is the user id, the inner key is the file id and the value is the developer knowledge about the file"
        const val LONGNAME_DEVELOPER_KNOWLEDGE = "--developer-knowledge"

        const val HELP_FILES_OWNERSHIP = "JSON file with map of maps, where the outer " +
                "key is the file id, the inner key is the user id and the value is the user data such owned lines and authorship"
        const val LONGNAME_FILES_OWNERSHIP = "--files-ownership"

        const val HELP_POTENTIAL_OWNERSHIP = "JSON file with map, where the " +
                "key is the file id and the value is potential authorship amount of all developers"
        const val LONGNAME_POTENTIAL_OWNERSHIP = "--potential-ownership"
    }

    private val local_resultDir = File("./result/FilesOwnershipMiner")

    private val developerKnowledgeJsonFile by saveFileOption(
        LONGNAME_DEVELOPER_KNOWLEDGE,
        HELP_DEVELOPER_KNOWLEDGE,
        File(local_resultDir, "DeveloperKnowledge.json")
    )

    private val filesOwnershipJsonFile by saveFileOption(
        LONGNAME_FILES_OWNERSHIP,
        HELP_FILES_OWNERSHIP,
        File(local_resultDir, "FilesOwnership.json")
    )

    private val potentialOwnershipJsonFile by saveFileOption(
        LONGNAME_POTENTIAL_OWNERSHIP,
        HELP_POTENTIAL_OWNERSHIP,
        File(local_resultDir, "PotentialAuthorship.json")
    )

    override fun idToFileOption() =
        saveFileOption(
            LONGNAME_ID_TO_FILE,
            mapperHelp("id", "file"), File(local_resultDir, "idToFile.json")
        )

    override fun idToUserOption() =
        saveFileOption(
            LONGNAME_ID_TO_USER,
            mapperHelp("id", "user"), File(local_resultDir, "idToUser.json")
        )

    private val idToUserJsonFile by idToUserOption()
    private val idToFileJsonFile by idToFileOption()

    override fun run() {
        val dataProcessor = FilesOwnershipDataProcessor()
        val miner = FilesOwnershipMiner(repositoryDirectory, branch, numThreads = numThreads)
        miner.run(dataProcessor)

        HelpFunctionsUtil.saveToJson(
            developerKnowledgeJsonFile,
            dataProcessor.developerKnowledge
        )
        HelpFunctionsUtil.saveToJson(
            filesOwnershipJsonFile,
            dataProcessor.filesOwnership
        )
        HelpFunctionsUtil.saveToJson(
            potentialOwnershipJsonFile,
            dataProcessor.potentialAuthorship
        )

        HelpFunctionsUtil.saveToJson(
            idToUserJsonFile,
            dataProcessor.idToUser
        )

        HelpFunctionsUtil.saveToJson(
            idToFileJsonFile,
            dataProcessor.idToFile
        )
    }
}