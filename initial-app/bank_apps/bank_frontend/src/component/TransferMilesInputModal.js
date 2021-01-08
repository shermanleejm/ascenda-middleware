import React, { useState } from "react";
import loyaltyProgramService from '../services/loyaltyProgramService';
import bankService from '../services/bankService';
import { Form, Input, Button, Tooltip, Card, Row, Col, Alert } from "antd";
import {
    GiftOutlined,
    ArrowLeftOutlined,
    InfoCircleOutlined,
} from "@ant-design/icons";

const TransferMilesInputModal = (props) => {
    const [rewardsAmount, setRewardsAmount] = useState(0);
    const [transferError, setTransferError] = useState(false);

    const onFinish = (values) => {
        console.log("Success:", values);
    };

    const onFinishFailed = (errorInfo) => {
        console.log("Failed:", errorInfo);
    };

    const onClickBack = () => {
        props.onChangeModalState("link");
    };
    
    const onInputAmount = (e) => {
        setRewardsAmount(e.target.value);
    };

    const onClickTransfer = () => {
        const currentDateISO = new Date().toISOString();
        const currentDate = currentDateISO.split("T")[0]
        const transferData = {
            loyalty_program_name: props.loyaltyProgram.loyaltyProgramName,
            member_id: props.membershipData.membershipNumber,
            first_name: props.user.firstName,
            last_name: props.user.lastName,
            transfer_date: currentDate,
            amount: Math.floor(rewardsAmount * (props.loyaltyProgram.ratio / 100)),
            bank_code: "dbs",
            misc: ""
        }
        newAccrualRequest(transferData)
        props.onSetTransferAmount(rewardsAmount);
    };

    const newAccrualRequest = (data) => {
        loyaltyProgramService.submitAccrualRequest(data).then((res) => {
            if(res){
                const transactionData = {
                    userId: 1,
                    memberId: props.membershipData.membershipNumber.toString(),
                    amount: Math.floor(rewardsAmount * (props.loyaltyProgram.ratio / 100)),
                    transactionCode: res["reference_number"]
                }
                bankService.addTransaction(transactionData)
                props.onSetReferenceNumber(res["reference_number"]);
                props.onChangeModalState("confirm");
            } else {
                setTransferError(true)
            }
        }).catch(e => {
            setTransferError(true)
        })
    }


    return (
        <div>
            <ArrowLeftOutlined
                style={{ fontSize: "20px", cursor: "pointer", float: "left" }}
                onClick={onClickBack}
            />
            <GiftOutlined style={{ fontSize: "60px", marginRight: "20px" }} />
            <h1>Transfer Your Miles</h1>
            <h4>
                Transfer your miles to your{" "}
                <b>{props.loyaltyProgram.loyaltyProgramName}</b> account:
            </h4>
            <h2>
                <b>
                    {props.membershipData.membershipNumber}
                    <Tooltip title="Account Number">
                        <InfoCircleOutlined
                            style={{
                                fontSize: "12px",
                                position: "relative",
                                right: "-5px",
                                top: "-5px",
                            }}
                        />
                    </Tooltip>
                </b>
            </h2>
            <Card style={{ background: "#F2F3F2" }}>
                <Row
                    style={{
                        display: "flex",
                        alignItems: "center",
                        justifyContent: "center",
                    }}
                >
                    <Col span={5}>
                        <div>
                            <span style={{ fontSize: "25px" }}>
                                {Number(
                                    props.user.pointBalance
                                ).toLocaleString()}
                            </span>
                            <br />
                            <span>AVAILABLE</span>
                        </div>
                    </Col>
                    <Col span={4} style={{ fontSize: "25px" }}>
                        -
                    </Col>
                    <Col span={5}>
                        <div>
                            <span style={{ fontSize: "25px" }}>
                                {rewardsAmount ? rewardsAmount : 0}
                            </span>
                            <br />
                            <span>USING</span>
                        </div>
                    </Col>
                    <Col span={4} style={{ fontSize: "25px" }}>
                        =
                    </Col>
                    <Col span={5}>
                        <div>
                            <span style={{ fontSize: "25px" }}>
                                {rewardsAmount
                                    ? (
                                          Number(props.user.pointBalance) -
                                          rewardsAmount
                                      ).toLocaleString()
                                    : Number(
                                          props.user.pointBalance
                                      ).toLocaleString()}
                            </span>
                            <br />
                            <span>REMAINING</span>
                        </div>
                    </Col>
                </Row>
            </Card>
            <Form
                name="transferMilesForm"
                layout="vertical"
                initialValues={{ remember: true }}
                onFinish={onFinish}
                onFinishFailed={onFinishFailed}
            >
                <Form.Item
                    name="rewardsAmount"
                    style={{ marginTop: "20px", textAlign: "center" }}
                    rules={[
                        {
                            message:
                                "Please input the amount you want to transfer!",
                        },
                    ]}
                >
                    <span>Total Rewards to Transfer</span>
                    <br />
                    <Input
                        type="number"
                        style={{ height: "50px", width: "50%" }}
                        onChange={(e) => onInputAmount(e)}
                    />
                    <br />
                    <span>{`Equates to ${
                        Math.floor(rewardsAmount * (props.loyaltyProgram.ratio / 100))
                    } ${props.loyaltyProgram.loyaltyProgramName} Points`}</span>
                </Form.Item>
                { 
                    transferError &&
                    <Alert
                        message="Oh no!"
                        description="Transaction failed! Please try again later."
                        style={{ marginTop: "10px", marginBottom: "20px" }}
                        type="error"
                    />
                }
                <Form.Item>
                    <Button
                        htmlType="submit"
                        style={{
                            background: "#197F20",
                            color: "#ffffff",
                            width: "70%",
                            height: "50px",
                        }}
                        onClick={onClickTransfer}
                    >
                        Complete Transfer
                    </Button>
                </Form.Item>
            </Form>
            <p>
                <b>All transfers are final.</b>
            </p>
            <p>
                Once rewards have been transferred, they are subject to the
                terms of the Loyalty Program to which they were transferred
            </p>
        </div>
    );
};

export default TransferMilesInputModal;
