package cli.gitMinersCLI

import cli.gitMinersCLI.base.GitMinerMultithreadedMultipleBranchesCLI
import dataProcessor.ChangedFilesDataProcessor
import miners.gitMiners.UserChangedFilesMiner
import util.HelpFunctionsUtil
import java.io.File

class ChangedFilesMinerCLI : GitMinerMultithreadedMultipleBranchesCLI(
    "ChangedFilesMiner",
    "Miner yields a $changedFilesByUsersHelp"
) {

    companion object {
        const val changedFilesByUsersHelp =
            "JSON file with a map, where key is the user id of a developer, " +
                    "and value is the list of file ids for the files edited by a developer."
        const val LONGNAME_CHANGED_FILES_BY_USER = "--changed-files-by-users"
    }

    private val local_resultDir = File("./result/ChangedFilesMiner")

    private val changedFilesByUsersJsonFile by saveFileOption(
        LONGNAME_CHANGED_FILES_BY_USER,
        changedFilesByUsersHelp,
        File(local_resultDir, "ChangedFilesByUser.json")
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
        val dataProcessor = ChangedFilesDataProcessor()
        val miner = UserChangedFilesMiner(repositoryDirectory, branches, numThreads = numThreads)
        miner.run(dataProcessor)

        HelpFunctionsUtil.saveToJson(
            changedFilesByUsersJsonFile,
            dataProcessor.changedFilesByUsers
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
