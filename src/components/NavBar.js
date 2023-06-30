import Container from "react-bootstrap/Container";
import Navbar from "react-bootstrap/Navbar";
import { Col, Row } from "react-bootstrap";
import "../assets/styles/styles.css";

function NavBar() {
  return (
    <Navbar bg="WHITE" variant="WHITE">
      <Container>
        <Navbar.Brand href="#home">
          <Row>
            <Col xs={2}>
              <img
                alt=""
                src={require("../assets/images/Logo.png")}
                width="86"
                height="54"
                className="d-inline-block align-top"
              />{" "}
            </Col>
            <Col xs={10}>
              <div>
                <p className="text-p">
                บีทามส์ &nbsp;
                  <span className="text-system">
                    คอมเพอร์เรอร์
                  </span>
                  {<br />}
                  <span className="text-english">
                  BComparer.
                  </span>
                </p>
              </div>
            </Col>
          </Row>
        </Navbar.Brand>
      </Container>
    </Navbar>
  );
}

export default NavBar;
