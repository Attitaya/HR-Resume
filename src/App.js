import React, { useState, useEffect } from "react";
import { useRef } from "react";
import axios from "axios";

import Swal from "sweetalert2";
import "./assets/styles/App.css";
import "bootstrap/dist/css/bootstrap.min.css";
import NavBar from "./components/NavBar";
import TextHolder from "./components/TextHolder";
import FileHolder from "./components/FileHolder";
//import MyTextarea from "./components/MyTextarea";
import { Container, Col, Button, Row } from "react-bootstrap";
// import swal from "sweetalert";

const titleData = [
  { id: 1, title: "หัวเรื่องจำแนกจากเอกสาร" },
  { id: 2, title: "NER ประเภทที่สนใจ" },
  { id: 3, title: "NER ประเภทที่ไม่ทราบแน่ชัด" },
];

const rootURL = "http://192.168.10.96:8787";
const extractedDataURL = `${rootURL}/upload`;
const essentialDataURL = `${rootURL}/essential_extract`;
const nerDataURL = `${rootURL}/ner_openai`;
const docDataURL = `${rootURL}/generate`;

function App() {
  const inputRef = useRef();
  const [itemsExtraction, setItemsExtraction] = useState([]);
  const [files, setFiles] = useState([]);
  const [filesResult, setFilesResult] = useState([]);
  const [message, setMessage] = useState("");
  const [essential, setEssential] = useState([{ text: "" }]);
  const [entityExtraction, setEntityExtraction] = useState([{ text: "" }]);
  const [formData, setFormData] = useState(new FormData());
  const [description, setDescription] = useState("");
  const [descriptionResult, setDescriptionResult] = useState("");
  const [uploadStatus, setUploadStatus] = useState(false);

  const handleDragOver = (event) => {
    event.preventDefault();
  };

  const handleDrop = async (event) => {
    event.preventDefault();
    const file = event.dataTransfer.files[0];
    console.log(event.dataTransfer.files);
    let formData = new FormData();
    formData.append("file", file);
    // Extract Document
    const extractedDoc = await axios({
      url: extractedDataURL,
      method: "POST",
      data: formData,
    });
    // Set FormData to state
    setFormData(formData);
    // Set selected file to state
    setFiles([file]);
    // Extract response data from first API call
    const extractedData = extractedDoc.data.result;
    // Make second API call Essential
    const essentialRes = await axios.post(essentialDataURL, {
      data: extractedData,
    });
    const essentialData = essentialRes.data.result.ess;
    setEssential([essentialData]);
    // Make third API call NER
    const nerRes = await axios.post(nerDataURL, { data: essentialData });
    const nerData = nerRes.data.result;
    setEntityExtraction([nerData]);
  };

  const handleExportToDatabae = () => {
    console.log("Export To Database...");
  };

  const titleData = [{ title: "Title 1" }, { title: "Title 2" }];

  const handleSubmit = async (event) => {
    console.log("handleSubmit...");
    console.log("description: ", description);
    console.log("files: ", files);

    const isDataComplete = description !== "" && files[0].name !== "";
    // const formattedValue = description.replace(/\n/g, '<br>');

    // setDescriptionResult(formattedValue);
    if (isDataComplete) {
      setUploadStatus(true);
      setDescriptionResult(description);
      setDescription("");
      setFiles([]);
      let formData = new FormData();
      files.forEach((file) => {
        formData.append("file", file);
      });
      // formData.append('file',files);
      formData.append("name", description);
      displaySuccess();
      displayFile(files);

      // // TODO-reset k val
      formData.append("k", 2);

      // extractedDoc = JSON.parse({
      //   "code": 200,
      //   "message": "Success",
      //   "reference": "",
      //   "results": "JobThai_5654196_\u0e13\u0e31\u0e10\u0e27\u0e38\u0e12\u0e34_\u0e27\u0e34\u0e15\u0e40\u0e2a\u0e16\u0e35\u0e22\u0e23.pdf\nRESUME \u0e44\u0e21\u0e48\u0e44\u0e14\u0e49\u0e43\u0e2b\u0e49\u0e02\u0e49\u0e2d\u0e21\u0e39\u0e25\u0e43\u0e14 \u0e46 \u0e17\u0e35\u0e48\u0e15\u0e23\u0e07\u0e01\u0e31\u0e1a JOBDESCRIPTION \u0e17\u0e33\u0e43\u0e2b\u0e49\u0e44\u0e21\u0e48\u0e40\u0e2b\u0e21\u0e32\u0e30\u0e01\u0e31\u0e1a\u0e07\u0e32\u0e19 \u0e02\u0e49\u0e2d\u0e21\u0e39\u0e25\u0e17\u0e35\u0e48\u0e23\u0e30\u0e1a\u0e38\u0e43\u0e19 RESUME \u0e19\u0e31\u0e49\u0e19\u0e04\u0e25\u0e38\u0e21\u0e40\u0e04\u0e23\u0e37\u0e2d\u0e41\u0e25\u0e30\u0e44\u0e21\u0e48\u0e21\u0e35\u0e04\u0e38\u0e13\u0e2a\u0e21\u0e1a\u0e31\u0e15\u0e34\u0e02\u0e2d\u0e07\u0e07\u0e32\u0e19\u0e17\u0e35\u0e48\u0e40\u0e01\u0e35\u0e48\u0e22\u0e27\u0e02\u0e49\u0e2d\u0e07 \u0e14\u0e31\u0e07\u0e19\u0e31\u0e49\u0e19\u0e04\u0e30\u0e41\u0e19\u0e19\u0e04\u0e27\u0e32\u0e21\u0e40\u0e2b\u0e21\u0e32\u0e30\u0e2a\u0e21\u0e01\u0e31\u0e1a\u0e07\u0e32\u0e19\u0e04\u0e37\u0e2d 1 \u0e40\u0e15\u0e47\u0e21 10\n\nJobThai_5372657_\u0e27\u0e34\u0e25\u0e32\u0e27\u0e31\u0e13\u0e22\u0e4c_\u0e40\u0e1b\u0e23\u0e21\u0e1e\u0e25.pdf\n\u0e19\u0e48\u0e32\u0e40\u0e2a\u0e35\u0e22\u0e14\u0e32\u0e22\u0e17\u0e35\u0e48\u0e44\u0e21\u0e48\u0e21\u0e35\u0e02\u0e49\u0e2d\u0e21\u0e39\u0e25\u0e2a\u0e33\u0e2b\u0e23\u0e31\u0e1a\u0e23\u0e32\u0e22\u0e25\u0e30\u0e40\u0e2d\u0e35\u0e22\u0e14\u0e02\u0e2d\u0e07\u0e07\u0e32\u0e19 \u0e14\u0e31\u0e07\u0e19\u0e31\u0e49\u0e19\u0e08\u0e36\u0e07\u0e40\u0e1b\u0e47\u0e19\u0e44\u0e1b\u0e44\u0e21\u0e48\u0e44\u0e14\u0e49\u0e17\u0e35\u0e48\u0e08\u0e30\u0e23\u0e30\u0e1a\u0e38\u0e04\u0e38\u0e13\u0e2a\u0e21\u0e1a\u0e31\u0e15\u0e34\u0e02\u0e2d\u0e07\u0e07\u0e32\u0e19\u0e17\u0e35\u0e48\u0e15\u0e49\u0e2d\u0e07\u0e01\u0e32\u0e23 \u0e2d\u0e22\u0e48\u0e32\u0e07\u0e44\u0e23\u0e01\u0e47\u0e15\u0e32\u0e21 \u0e08\u0e32\u0e01\u0e02\u0e49\u0e2d\u0e21\u0e39\u0e25\u0e17\u0e35\u0e48\u0e43\u0e2b\u0e49\u0e44\u0e27\u0e49\u0e43\u0e19\u0e40\u0e23\u0e0b\u0e39\u0e40\u0e21\u0e48 \u0e1b\u0e23\u0e32\u0e01\u0e0f\u0e27\u0e48\u0e32\u0e1c\u0e39\u0e49\u0e2a\u0e21\u0e31\u0e04\u0e23\u0e21\u0e35\u0e1b\u0e23\u0e30\u0e2a\u0e1a\u0e01\u0e32\u0e23\u0e13\u0e4c\u0e43\u0e19\u0e01\u0e32\u0e23\u0e41\u0e01\u0e49\u0e44\u0e02\u0e1b\u0e31\u0e0d\u0e2b\u0e32\u0e04\u0e2d\u0e21\u0e1e\u0e34\u0e27\u0e40\u0e15\u0e2d\u0e23\u0e4c \u0e01\u0e32\u0e23\u0e40\u0e02\u0e35\u0e22\u0e19\u0e42\u0e1b\u0e23\u0e41\u0e01\u0e23\u0e21 \u0e41\u0e25\u0e30\u0e01\u0e32\u0e23\u0e43\u0e0a\u0e49\u0e42\u0e1b\u0e23\u0e41\u0e01\u0e23\u0e21 Microsoft Office \u0e1e\u0e27\u0e01\u0e40\u0e02\u0e32\u0e22\u0e31\u0e07\u0e21\u0e35\u0e1b\u0e23\u0e30\u0e2a\u0e1a\u0e01\u0e32\u0e23\u0e13\u0e4c\u0e43\u0e19\u0e01\u0e32\u0e23\u0e2d\u0e2d\u0e01\u0e41\u0e1a\u0e1a\u0e23\u0e30\u0e1a\u0e1a\u0e08\u0e31\u0e14\u0e01\u0e32\u0e23\u0e2b\u0e2d\u0e1e\u0e31\u0e01\u0e41\u0e25\u0e30\u0e27\u0e32\u0e14\u0e20\u0e32\u0e1e\u0e41\u0e1f\u0e19\u0e2d\u0e32\u0e23\u0e4c\u0e15\u0e14\u0e49\u0e27\u0e22\u0e42\u0e1b\u0e23\u0e41\u0e01\u0e23\u0e21 Adobe Illustrator \u0e22\u0e31\u0e07\u0e44\u0e21\u0e48\u0e0a\u0e31\u0e14\u0e40\u0e08\u0e19\u0e27\u0e48\u0e32\u0e17\u0e31\u0e01\u0e29\u0e30\u0e40\u0e2b\u0e25\u0e48\u0e32\u0e19\u0e35\u0e49\u0e40\u0e01\u0e35\u0e48\u0e22\u0e27\u0e02\u0e49\u0e2d\u0e07\u0e01\u0e31\u0e1a\u0e23\u0e32\u0e22\u0e25\u0e30\u0e40\u0e2d\u0e35\u0e22\u0e14\u0e07\u0e32\u0e19\u0e2d\u0e22\u0e48\u0e32\u0e07\u0e44\u0e23 \u0e2b\u0e32\u0e01\u0e44\u0e21\u0e48\u0e21\u0e35\u0e23\u0e32\u0e22\u0e25\u0e30\u0e40\u0e2d\u0e35\u0e22\u0e14\u0e07\u0e32\u0e19\u0e43\u0e2b\u0e49\u0e40\u0e1b\u0e23\u0e35\u0e22\u0e1a\u0e40\u0e17\u0e35\u0e22\u0e1a \u0e01\u0e32\u0e23\u0e1b\u0e23\u0e30\u0e40\u0e21\u0e34\u0e19\u0e04\u0e27\u0e32\u0e21\u0e40\u0e2b\u0e21\u0e32\u0e30\u0e2a\u0e21\u0e02\u0e2d\u0e07\u0e1c\u0e39\u0e49\u0e2a\u0e21\u0e31\u0e04\u0e23\u0e2a\u0e33\u0e2b\u0e23\u0e31\u0e1a\u0e07\u0e32\u0e19\u0e19\u0e31\u0e49\u0e19\u0e17\u0e33\u0e44\u0e14\u0e49\u0e22\u0e32\u0e01\n\nJobThai_5372657_\u0e27\u0e34\u0e25\u0e32\u0e27\u0e31\u0e13\u0e22\u0e4c_\u0e40\u0e1b\u0e23\u0e21\u0e1e\u0e25.pdf\nRESUME \u0e44\u0e21\u0e48\u0e44\u0e14\u0e49\u0e43\u0e2b\u0e49\u0e02\u0e49\u0e2d\u0e21\u0e39\u0e25\u0e40\u0e1e\u0e35\u0e22\u0e07\u0e1e\u0e2d\u0e17\u0e35\u0e48\u0e08\u0e30\u0e1e\u0e34\u0e08\u0e32\u0e23\u0e13\u0e32\u0e27\u0e48\u0e32\u0e2a\u0e2d\u0e14\u0e04\u0e25\u0e49\u0e2d\u0e07\u0e2b\u0e23\u0e37\u0e2d\u0e40\u0e2b\u0e21\u0e32\u0e30\u0e2a\u0e21\u0e01\u0e31\u0e1a\u0e04\u0e38\u0e13\u0e2a\u0e21\u0e1a\u0e31\u0e15\u0e34\u0e02\u0e2d\u0e07\u0e07\u0e32\u0e19\u0e43\u0e19 JOBDESCRIPTION \u0e2b\u0e23\u0e37\u0e2d\u0e44\u0e21\u0e48 \u0e40\u0e19\u0e37\u0e48\u0e2d\u0e07\u0e08\u0e32\u0e01\u0e44\u0e21\u0e48\u0e21\u0e35 JOBDESCRIPTION \u0e14\u0e31\u0e07\u0e19\u0e31\u0e49\u0e19\u0e08\u0e36\u0e07\u0e44\u0e21\u0e48\u0e2a\u0e32\u0e21\u0e32\u0e23\u0e16\u0e1b\u0e23\u0e30\u0e40\u0e21\u0e34\u0e19\u0e04\u0e27\u0e32\u0e21\u0e40\u0e2b\u0e21\u0e32\u0e30\u0e2a\u0e21\u0e01\u0e31\u0e1a\u0e07\u0e32\u0e19\u0e23\u0e30\u0e2b\u0e27\u0e48\u0e32\u0e07 RESUME \u0e41\u0e25\u0e30 JOBDESCRIPTION \u0e42\u0e14\u0e22\u0e43\u0e2b\u0e49\u0e04\u0e30\u0e41\u0e19\u0e19\u0e08\u0e32\u0e01 1-10\n\nJobThai_3817591_\u0e27\u0e23\u0e40\u0e0a\u0e29\u0e10\u0e4c_\u0e27\u0e07\u0e28\u0e4c\u0e44\u0e0a\u0e22\u0e17\u0e32.pdf\nRESUME \u0e41\u0e2a\u0e14\u0e07\u0e23\u0e32\u0e22\u0e01\u0e32\u0e23\u0e1b\u0e23\u0e30\u0e2a\u0e1a\u0e01\u0e32\u0e23\u0e13\u0e4c\u0e43\u0e19\u0e01\u0e32\u0e23\u0e1e\u0e31\u0e12\u0e19\u0e32\u0e41\u0e25\u0e30\u0e40\u0e02\u0e35\u0e22\u0e19\u0e42\u0e1b\u0e23\u0e41\u0e01\u0e23\u0e21\u0e23\u0e30\u0e1a\u0e1a\u0e44\u0e2d\u0e17\u0e35 \u0e0b\u0e36\u0e48\u0e07\u0e2a\u0e2d\u0e14\u0e04\u0e25\u0e49\u0e2d\u0e07\u0e01\u0e31\u0e1a\u0e15\u0e33\u0e41\u0e2b\u0e19\u0e48\u0e07\u0e07\u0e32\u0e19\u0e17\u0e35\u0e48\u0e15\u0e49\u0e2d\u0e07\u0e01\u0e32\u0e23\u0e02\u0e2d\u0e07 Front-End, Back-End \u0e41\u0e25\u0e30 Fu\u0e19\u0e31\u0e01\u0e1e\u0e31\u0e12\u0e19\u0e32 ll-Stack \u0e2d\u0e22\u0e48\u0e32\u0e07\u0e44\u0e23\u0e01\u0e47\u0e15\u0e32\u0e21 \u0e40\u0e01\u0e23\u0e14\u0e40\u0e09\u0e25\u0e35\u0e48\u0e22 2.22 \u0e2d\u0e32\u0e08\u0e44\u0e21\u0e48\u0e15\u0e23\u0e07\u0e15\u0e32\u0e21\u0e04\u0e38\u0e13\u0e2a\u0e21\u0e1a\u0e31\u0e15\u0e34\u0e02\u0e2d\u0e07\u0e19\u0e32\u0e22\u0e08\u0e49\u0e32\u0e07\u0e1a\u0e32\u0e07\u0e23\u0e32\u0e22 \u0e40\u0e07\u0e34\u0e19\u0e40\u0e14\u0e37\u0e2d\u0e19\u0e17\u0e35\u0e48\u0e15\u0e49\u0e2d\u0e07\u0e01\u0e32\u0e23 40,000 \u0e2d\u0e22\u0e39\u0e48\u0e43\u0e19\u0e0a\u0e48\u0e27\u0e07\u0e17\u0e35\u0e48\u0e01\u0e33\u0e2b\u0e19\u0e14\u0e43\u0e19 JOBDESCRIPTION \u0e42\u0e14\u0e22\u0e23\u0e27\u0e21\u0e41\u0e25\u0e49\u0e27 RESUME \u0e04\u0e48\u0e2d\u0e19\u0e02\u0e49\u0e32\u0e07\u0e40\u0e2b\u0e21\u0e32\u0e30\u0e2a\u0e21\u0e01\u0e31\u0e1a\u0e07\u0e32\u0e19 \u0e42\u0e14\u0e22\u0e43\u0e2b\u0e49\u0e04\u0e30\u0e41\u0e19\u0e19 6 \u0e40\u0e15\u0e47\u0e21 10\n\nJobThai_5654196_\u0e13\u0e31\u0e10\u0e27\u0e38\u0e12\u0e34_\u0e27\u0e34\u0e15\u0e40\u0e2a\u0e16\u0e35\u0e22\u0e23.pdf\nRESUME \u0e41\u0e2a\u0e14\u0e07\u0e23\u0e32\u0e22\u0e01\u0e32\u0e23\u0e20\u0e32\u0e29\u0e32\u0e42\u0e1b\u0e23\u0e41\u0e01\u0e23\u0e21\u0e41\u0e25\u0e30\u0e1b\u0e23\u0e30\u0e2a\u0e1a\u0e01\u0e32\u0e23\u0e13\u0e4c\u0e43\u0e19\u0e01\u0e32\u0e23\u0e1e\u0e31\u0e12\u0e19\u0e32\u0e40\u0e27\u0e47\u0e1a\u0e44\u0e0b\u0e15\u0e4c \u0e0b\u0e36\u0e48\u0e07\u0e2a\u0e2d\u0e14\u0e04\u0e25\u0e49\u0e2d\u0e07\u0e01\u0e31\u0e1a\u0e15\u0e33\u0e41\u0e2b\u0e19\u0e48\u0e07\u0e07\u0e32\u0e19\u0e02\u0e2d\u0e07\u0e42\u0e1b\u0e23\u0e41\u0e01\u0e23\u0e21\u0e40\u0e21\u0e2d\u0e23\u0e4c\u0e43\u0e19 JOBDESCRIPTION \u0e2d\u0e22\u0e48\u0e32\u0e07\u0e44\u0e23\u0e01\u0e47\u0e15\u0e32\u0e21 \u0e40\u0e01\u0e23\u0e14\u0e40\u0e09\u0e25\u0e35\u0e48\u0e22 2.23 \u0e2d\u0e32\u0e08\u0e44\u0e21\u0e48\u0e15\u0e23\u0e07\u0e15\u0e32\u0e21\u0e04\u0e38\u0e13\u0e2a\u0e21\u0e1a\u0e31\u0e15\u0e34\u0e17\u0e35\u0e48\u0e23\u0e30\u0e1a\u0e38\u0e44\u0e27\u0e49\u0e43\u0e19 JOBDESCRIPTION RESUME \u0e22\u0e31\u0e07\u0e23\u0e27\u0e21\u0e16\u0e36\u0e07\u0e1b\u0e23\u0e30\u0e2a\u0e1a\u0e01\u0e32\u0e23\u0e13\u0e4c\u0e01\u0e32\u0e23\u0e17\u0e33\u0e07\u0e32\u0e19\u0e43\u0e19\u0e2d\u0e38\u0e15\u0e2a\u0e32\u0e2b\u0e01\u0e23\u0e23\u0e21\u0e15\u0e48\u0e32\u0e07\u0e46 \u0e2d\u0e35\u0e01\u0e14\u0e49\u0e27\u0e22 \u0e41\u0e15\u0e48\u0e22\u0e31\u0e07\u0e44\u0e21\u0e48\u0e0a\u0e31\u0e14\u0e40\u0e08\u0e19\u0e27\u0e48\u0e32\u0e21\u0e35\u0e04\u0e27\u0e32\u0e21\u0e40\u0e01\u0e35\u0e48\u0e22\u0e27\u0e02\u0e49\u0e2d\u0e07\u0e01\u0e31\u0e1a\u0e07\u0e32\u0e19\u0e17\u0e35\u0e48\u0e15\u0e49\u0e2d\u0e07\u0e01\u0e32\u0e23\u0e2d\u0e22\u0e48\u0e32\u0e07\u0e44\u0e23 \u0e42\u0e14\u0e22\u0e23\u0e27\u0e21\u0e41\u0e25\u0e49\u0e27 RESUME \u0e15\u0e23\u0e07\u0e01\u0e31\u0e1a JOBDESCRIPTION \u0e1a\u0e32\u0e07\u0e2a\u0e48\u0e27\u0e19 \u0e41\u0e25\u0e30\u0e08\u0e30\u0e43\u0e2b\u0e49\u0e04\u0e30\u0e41\u0e19\u0e19 6 \u0e40\u0e15\u0e47\u0e21 10 \u0e2a\u0e33\u0e2b\u0e23\u0e31\u0e1a\u0e04\u0e27\u0e32\u0e21\u0e40\u0e2b\u0e21\u0e32\u0e30\u0e2a\u0e21",
      //   "status": true
      // })

      const extractedDoc = await axios({
        url: extractedDataURL,
        method: "POST",
        data: formData,
      });

      setDescription("");
      setDescriptionResult(extractedDoc.data.results);
      // setFiles("");
    } else {
      setUploadStatus(false);
      setDescription("");
      setDescriptionResult("");
      // setReloadFile("");
      // setFiles("");
      displayError();
    }
  };

  // Function to display error message
  const displayError = () => {
    Swal.fire({
      icon: "error",
      title: "Oops...",
      text: "Please put your File and Text",
    });
  };
  // Function to display success message
  const displaySuccess = () => {
    Swal.fire({
      position: "center",
      icon: "success",
      title: "Your Files and Text has been saved.",
      showConfirmButton: false,
      timer: 1500,
    });
  };
  const displayFile = (files) => {
    let set_message = "";
    for (let i = 0; i < files.length; i++) {
      const file = files[i];
      set_message += `ไฟล์ที่ ${i + 1} คือ: ${file.name} \n`;
      console.log(set_message); // หรือทำการแสดงผลใน DOM ตามที่คุณต้องการ
    }

    setMessage(set_message);
  };

  return (
    <div>
      <NavBar></NavBar>
      <Container className="containerCard">
        <Row>
          <Col xs={12}>
            <Container className="container-card">
              <Row>
                <Col xs={4}>
                  <div className="d-flex flex-column align-items-end">
                    <div
                      className="dropzone w-100"
                      onDragOver={handleDragOver}
                      onDrop={handleDrop}
                    >
                      <img
                        alt=""
                        src={require("./assets/images/upload_1.png")}
                        width="100"
                        height="77"
                        className="d-inline-block align-top"
                      />{" "}
                      <h3 className="text-files">Drag and Drop Files Here</h3>
                      <div className="containerd">
                        <div className="fileUploadInput">
                          <input
                            type="file"
                            onChange={(event) =>
                              setFiles(Array.from(event.target.files))
                            }
                            ref={inputRef}
                            accept=".pdf"
                            // value={files}
                            multiple
                          />
                          <button>+</button>
                        </div>
                      </div>
                    </div>
                    <div className="box-btn">
                    </div>
                    <div className="text-box w-100">
                      <textarea
                        className="custom-textarea"
                        id="description"
                        name="description"
                        placeholder="กรุณากรอกข้อมูลรายละเอียด"
                        value={description}
                        onChange={(event) => setDescription(event.target.value)}
                      ></textarea>
                      {/* <p>{descriptionResult}</p> */}
                    </div>

                    <Button
                      className="btn btn-send"
                      id="submitButton"
                      type="button"
                      onClick={(e) => handleSubmit()}
                    >
                      submit
                    </Button>
                  </div>
                </Col>
                <Col xs={8}>
                  {essential[0].text !== "" ? (
                    <div>
                      <TextHolder
                        mTitle={titleData[0]["title"]}
                        textObj={essential[0]}
                        setItemsExtraction={setItemsExtraction}
                        endPoint={1}
                      />
                      <TextHolder
                        mTitle={titleData[1]["title"]}
                        textObj={entityExtraction[0]}
                        setItemsExtraction={setItemsExtraction}
                        endPoint={2}
                      />
                      <FileHolder
                        mTitle={titleData[0]["title"]}
                        textObj={essential[0]}
                        setItemsExtraction={setFilesResult}
                        endPoint={1}
                      />
                      <FileHolder
                        mTitle={titleData[1]["title"]}
                        textObj={entityExtraction[0]}
                        setFilesResult={setFilesResult}
                        endPoint={2}
                      />
                    </div>
                  ) : (
                    <h3>กรุณากรอกข้อมูลทางด้านซ้ายมือ</h3>
                  )}
                  <div className="text-box w-100">
                    <textarea
                      className="receiving-box"
                      value={message}
                      onChange={(event) => setFiles(event.target.value)}
                      style={{
                        height: "150px",
                        overflowY: "scroll",
                        // position: 'absolute',
                        resize: "none",
                        width: "100%",
                        padding: "10px",
                        border: "1px solid #fff",
                        borderRadius: "4px",
                        fontFamily: "Sarabun, sans-serif",
                        fontSize: "16px",
                        bottom: 0,
                      }}
                    ></textarea>
                    {/* <p>{descriptionResult}</p> */}
                  </div>
                  <div className="text-box w-100">
                    <textarea
                      className="receiving-box"
                      value={descriptionResult}
                      onChange={(event) => setDescription(event.target.value)}
                      style={{
                        height: "320px",
                        overflowY: "scroll",
                        // position: 'absolute',
                        resize: "none",
                        width: "100%",
                        padding: "10px",
                        border: "1px solid #fff",
                        borderRadius: "4px",
                        fontFamily: "Sarabun, sans-serif",
                        fontSize: "16px",
                        bottom: 0,
                      }}
                    ></textarea>
                    {/* <p>{descriptionResult}</p> */}
                  </div>
                </Col>
              </Row>
            </Container>
          </Col>
        </Row>
      </Container>
    </div>
  );
}

export default App;
