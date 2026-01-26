import ResultsList from "./ResultsList"
import Upload from "./Upload"

export default function Container(){
    return (
        <div className="bg-gray-800/40 p-5 rounded-lg outline outline-gray-700/50 backdrop-blur-sm text-white gap-8 flex flex-col">
            <Upload />
            <ResultsList />
            </div>
    )
}