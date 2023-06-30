
import DragDropFiles from "../components/DragDropFiles";
import TextHolder from "../components/TextHolder";

const titleData = [
    {
        "id": 1,
        "title": "หัวเรื่องจำแนกจากเอกสาร"
    },
    {
        "id": 2,
        "title": "NER ประเภทที่สนใจ"
    },
    {
        "id": 3,
        "title": "NER ประเภทที่ไม่ทราบแน่ชัด"
    },
]


const DocumentReaderPage = () => {
    return (
        <>
            <br></br>
            <div className='container'>
                <div className="row">
                    <div className="column">
                        <DragDropFiles></DragDropFiles>
                    </div>
                    <div className="column">
                        {
                            titleData.map(titleData => (
                                <TextHolder
                                id={titleData.id}
                                title={titleData.title}
                                />
                            ))
                        }
                    </div>
                </div>
            </div>
        </>
    )
}

export default DocumentReaderPage;