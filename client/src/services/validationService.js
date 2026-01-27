import axios from "axios";

export async function validateImage(files, setProgress) {
    const formData = new FormData();

    Array.from(files).forEach(file => {
        formData.append("files", file);
    })

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