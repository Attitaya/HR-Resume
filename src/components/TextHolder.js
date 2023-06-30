import Card from 'react-bootstrap/Card';
import React, { useEffect, useState } from "react";
import { Button } from 'react-bootstrap';
import axios from "axios";
import swal from 'sweetalert';

const rootURL = "http://localhost:8899";
const essDatabaseURL = `${rootURL}/add_ess_data`;
const nerDatabaseURL = `${rootURL}/add_ner_data`;

export function TextHolder({ mTitle, textObj, setItemsExtraction, endPoint }) {

  const [selected, setSelected] = useState([])
  const [dataExtraction, setDataExtraction] = useState([]);
  const [description, setDescription] = useState("");
  var data = textObj;

  // const handleCheckboxChange = (event, index, key, type) => {
  //   console.log("type:", type);
  //   const checkboxId = index;
  //   const isChecked = event.target.checked;
  //   const setData = { [key]: textObj[key] }
  //   setSelected((prevState) =>
  //     prevState.map((checkbox) =>
  //       checkbox.id === checkboxId ? { ...checkbox, checked: isChecked } : checkbox
  //     )
  //   );
  //   if (isChecked) {
  //     setDataExtraction(prevData => [...prevData, setData]);
  //   } else {
  //     setDataExtraction(dataExtraction.filter(values => Object.keys(values) != key))
  //   }
  // };

  const handleExportToDatabase = async (type) => {
    console.log("Describtion:", description);
    setDescription(description);
    const params = {
      description: description
    }
    if (endPoint === 1) {    
      await axios({
        url: essDatabaseURL,
        method: "POST",
        data: params
      })
      swal("Done!", "Add to Database!", "success");
    }
    else if (endPoint === 2) {
      
      await axios({
        url: nerDatabaseURL,
        method: "POST",
        data: params
      })
    }
    swal("Done!", "Add to Database!", "success");

  };

  return (
    <div>
      <Card className='card-items'>
        <h3 className='title-type'>{mTitle}</h3>
        <hr />
        {/* {
          Object.entries(data).map((key, val) =>
            <div className="checkbox-item2" key={mTitle + "-" + key[0]}>
              <input id={mTitle + "-" + key[0]} type="checkbox" value={key[0]} onChange={(e) => handleCheckboxChange(e, mTitle + "-" + key[0], key[0], mTitle)} checked={val.checked} style={{ marginRight: '1%' }} />
              <span>{key[0]} : {key[1]}</span>
            </div>
          )
        } */}
        <Button className='btn-save btn-template' variant="outline-primary" onClick={(e) => handleExportToDatabase()}>
          <span className='icons-message'>Save to Database</span>
        </Button>
      </Card>
    </div>
  );
}

export default TextHolder;