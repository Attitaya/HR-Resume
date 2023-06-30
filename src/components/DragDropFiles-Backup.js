import { useRef } from "react";
import axios from "axios";

const rootURL = "http://192.168.10.96:8787";
const extractedDataURL = `${rootURL}/upload`;


const DragDropFiles = ({files, setFiles, essential, setEssential, entityExtraction, setEntityExtraction, outEntity, setOutEntity}) => {
    const inputRef = useRef();

    const handleDragOver = (event) => {
        event.preventDefault();
    };

    const handleDrop = async (event) => {
        event.preventDefault();
        const file = event.dataTransfer.files[0];
        let formData = new FormData()
        formData.append('file', file);
        // Extract Document
        const extractedDoc = await axios({
            url: extractedDataURL,
            method: "POST",
            data: formData
        })
        // Extract response data from first API call
        const extractedData = extractedDoc.data.result;
        // Make second API call Essential
        const essentialRes = await axios.post(essentialDataURL, { data: extractedData });      
        const essentialData = essentialRes.data.result.ess;
        setEssential([essentialData])
        // Make third API call NER
        const nerRes = await axios.post(nerDataURL, { data: essentialData });
        const nerData = nerRes.data.result;
        setEntityExtraction([nerData])
    };

    return (
        <>
            {
                <div className="dropzone" onDragOver={handleDragOver} onDrop={handleDrop}>
                    <img alt="" src={require('./upload.png')} width="100" height="100" className="d-inline-block align-top" />{' '}
                    <h3 className="text-files">Drag and Drop Files Here</h3>
                    <input type="file" onChange={(event) => setFiles(event.target.files)} hidden ref={inputRef}/>
                </div>
            }
        </>
    )
}

export default DragDropFiles;