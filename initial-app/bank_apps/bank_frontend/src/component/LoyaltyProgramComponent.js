import React, { useState } from 'react';
import { Card, Row, Col } from "antd";
import TransferMilesModal from './TransferMilesModal';

const LoyaltyProgramComponent = (props) => {
    const [modalVisible, setModalVisible] = useState(false);

    const showModal = () => {
        setModalVisible(true);
    };

    const handleOk = (e) => {
        setModalVisible(false);
    };

    const handleCancel = (e) => {
        setModalVisible(false);
    };
    
    return (
        <>
            <Card>
                <Row>
                    <Col span={6}>
                        <img
                            src="https://icm.aexp-static.com/loyalty/lsm/product19547.png"
                            width="200"
                        />
                    </Col>
                    <Col span={16}>
                        <h3>{props.loyaltyProgram.loyaltyProgramName}</h3>
                        <span>1000 ABC Points = {1000 * (props.loyaltyProgram.ratio / 100)} {props.loyaltyProgram.loyaltyProgramName} Points</span>
                        <br/>
                        <span>Estimated transfer time: {props.loyaltyProgram.processingTime}</span>
                        <br/>
                        <a href={"https://www." + props.loyaltyProgram.enrollmentLink} target="__blank" style={{marginRight: "20px"}}>Enrollment Details</a>
                        <a href={"https://www." + props.loyaltyProgram.termsAndConditionsLink} target="__blank">Terms and Conditions</a>
                    </Col>
                    <a onClick={showModal}>Transfer Miles</a>
                </Row>
            </Card>
            <TransferMilesModal
                user={props.user}
                loyaltyProgram={props.loyaltyProgram}
                visible={modalVisible}
                handleOk={handleOk}
                handleCancel={handleCancel}
            />
        </>
    );
}

export default LoyaltyProgramComponent;
