package cli.gitMinersCLI

import cli.gitMinersCLI.base.GitMinerMultithreadedMultipleBranchesCLI
import dataProcessor.CommitInfluenceGraphDataProcessor
import miners.gitMiners.CommitInfluenceGraphMiner
import org.eclipse.jgit.internal.storage.file.FileRepository
import util.HelpFunctionsUtil
import java.io.File

class CommitInfluenceGraphMinerCLI : GitMinerMultithreadedMultipleBranchesCLI(
    "CommitInfluenceGraphMiner",
    "Miner yields the $HELP_COMMITS_GRAPH"
) {
    companion object {
        const val HELP_COMMITS_GRAPH = "JSON file  with a map of lists, with key corresponding to the fixing " +
                "commit id and value corresponding to the commits with lines changed by fixes."
        const val LONGNAME_COMMITS_GRAPH = "--commits-graph"
    }

    private val local_resultDir = File("./result/CommitInfluenceGraphMiner")

    override fun idToCommitOption() =
        saveFileOption(
            LONGNAME_ID_TO_COMMIT,
            mapperHelp("id", "commit"), File(local_resultDir, "idToCommit.json")
        )

    private val commitsGraphJsonFile by saveFileOption(
        LONGNAME_COMMITS_GRAPH,
        HELP_COMMITS_GRAPH,
        File(local_resultDir, "CommitInfluenceGraph.json")
    )

    private val idToCommitJsonFile by idToCommitOption()

    override fun run() {
        val dataProcessor = CommitInfluenceGraphDataProcessor()
        val miner = CommitInfluenceGraphMiner(repositoryDirectory, branches, numThreads = numThreads)
        miner.run(dataProcessor)

        HelpFunctionsUtil.saveToJson(
            commitsGraphJsonFile,
            dataProcessor.adjacencyMap
        )

        HelpFunctionsUtil.saveToJson(
            idToCommitJsonFile,
            dataProcessor.idToCommit
        )
    }
}
