import axios from "axios";

export async function validateImage(file, setProgress, setLoading) {
    const formData = new FormData();
    formData.append("file", file);

    setLoading(true);
    setProgress(0);

    try {
        const response = await axios.post(
            "http://localhost:8000/api/validate",
            formData,
            {
                headers: {
                    "Content-Type": "multipart/form-data",
                },
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
    } finally {
        setLoading(false);
    }
}