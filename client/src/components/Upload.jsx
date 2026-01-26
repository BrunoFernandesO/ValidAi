export default function Upload(){
    return (
      <div className="flex flex-col justify-center items-center bg-black/20 outline outline-gray-700/50 backdrop-blur-sm text-gray-400 text-lg xl:text-lg px-8 py-20 rounded-lg border-2 border-dashed border-gray-600 cursor-pointer hover:border-gray-500 hover:bg-black/15 transition-colors text-center">
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-16 mb-2">
  <path stroke-linecap="round" stroke-linejoin="round" d="M12 16.5V9.75m0 0 3 3m-3-3-3 3M6.75 19.5a4.5 4.5 0 0 1-1.41-8.775 5.25 5.25 0 0 1 10.233-2.33 3 3 0 0 1 3.758 3.848A3.752 3.752 0 0 1 18 19.5H6.75Z" />
</svg>

                  <p className="w-100 xl:w-80">Arraste e solte seus arquivos ou pasta aqui, ou clique para selecionar</p>
      </div>
    )
}