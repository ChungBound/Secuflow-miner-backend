package cli.gitMinersCLI

import cli.gitMinersCLI.base.GitMinerMultithreadedMultipleBranchesCLI
import dataProcessor.AssignmentMatrixDataProcessor
import miners.gitMiners.UserChangedFilesMiner
import util.HelpFunctionsUtil
import java.io.File

class AssignmentMatrixMinerCLI :
    GitMinerMultithreadedMultipleBranchesCLI
        (
        "AssignmentMatrixMiner",
        "Miner yields a $HELP_ASSIGNMENT_MATRIX"
    ) {

    companion object {
        const val HELP_ASSIGNMENT_MATRIX =
            "JSON file with map of maps, where outer key is the user id, " +
                    "inner key is the file id and the value is the number of times the user has edited the file."
        const val LONGNAME_ASSIGNMENT_MATRIX = "--assignment-matrix"
    }

    private val local_resultDir = File("./result/AssignmentMatrixMiner")

    private val assignmentMatrixJsonFile by saveFileOption(
        LONGNAME_ASSIGNMENT_MATRIX,
        HELP_ASSIGNMENT_MATRIX,
        File(local_resultDir, "AssignmentMatrix.json")
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
        val dataProcessor = AssignmentMatrixDataProcessor()
        val miner = UserChangedFilesMiner(repositoryDirectory, branches, numThreads = numThreads)
        miner.run(dataProcessor)

        HelpFunctionsUtil.saveToJson(
            assignmentMatrixJsonFile,
            dataProcessor.assignmentMatrix
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
