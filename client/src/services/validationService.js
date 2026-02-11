import axios from "axios";

export async function validateImage(files, setProgress, filters) {
    console.log("🔥 validateImage called with filters: ", filters);
    const formData = new FormData();

    Array.from(files).forEach(file => {
        formData.append("files", file);
    })

    if (filters.masSize != null) {
        console.log("Adding max_size to formData: ", filters.max_size);
        formData.append("max_size", filters.max_size);
    }
    if (filters.expected_width != null) {
        console.log("Adding expected_width to formData: ", filters.expected_width);
        formData.append("expected_width", filters.expected_width);
    }
    if (filters.expected_height != null) {
        console.log("Adding expected_height to formData: ", filters.expected_height);
        formData.append("expected_height", filters.expected_height);
    }
    if (filters.expected_extensions != null) {
        console.log("Adding expected_extensions to formData: ", filters.expected_extensions);
        formData.append("expected_extensions", filters.expected_extensions);
    }


    setProgress(0);

    try {
        const response = await axios.post(
            "http://localhost:8000/api/validate",
            formData,
            {
                onUploadProgress: (event) => {
                    if (!event.total) return;

                    const percent = Math.round(
                        (event.loaded * 100) / event.total
                    );

                    setProgress(percent);
                }
            }
        )
        return response.data;
    } catch (error) {
        console.error("validateImage error: ", error);
        throw error;
    }
}