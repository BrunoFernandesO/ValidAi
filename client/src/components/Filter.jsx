import InputSelectBase from "./InputSelectBase";

export default function Filter({ handleFilters }) {

  return (
    <div className="flex justify-between">
      <InputSelectBase
        as="input"
        type="text"
        name="max_size"
        label="Tamanho máximo (MB)"
        required={true}
        placeholder="Ex: 5"
        onChange={handleFilters}
      ></InputSelectBase>

      <div className="flex gap-5">
        <InputSelectBase
          as="input"
          type="text"
          name="expected_width"
          label="Largura (px)"
          required={false}
          placeholder="Ex: 1920"
          onChange={handleFilters}
        ></InputSelectBase>

        <InputSelectBase
          as="input"
          type="text"
          name="expected_height"
          label="Altura (px)"
          required={false}
          placeholder="Ex: 1080"
          onChange={handleFilters}
        ></InputSelectBase>
      </div>

      <InputSelectBase
        as="select"
        name="expected_extensions"
        label="Formato esperado"
        required={false}
        onChange={handleFilters}
      >
        <option value="" className="bg-gray-800">
          Não filtrar
        </option>
        <option value="jpg" className="bg-gray-800">
          jpg
        </option>
        <option value="jpeg" className="bg-gray-800">
          jpeg
        </option>
        <option value="png" className="bg-gray-800">
          png
        </option>
      </InputSelectBase>
    </div>
  );
}
