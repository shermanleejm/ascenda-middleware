import React, { useState } from "react";
import loyaltyProgramService from '../services/loyaltyProgramService';
import { Form, Input, Button, Alert } from "antd";
import { GiftOutlined } from "@ant-design/icons";

const TransferMilesLinkModal = (props) => {
    const [membershipNumber, setMembershipNumber] = useState()
    const [membershipValidationError, setMembershipValidationError] = useState(false)

    const onFinish = (values) => {
        console.log("Success:", values);
    };

    const onFinishFailed = (errorInfo) => {
        console.log("Failed:", errorInfo);
    };

    const onClickSaveMembership = () => {
        const membershipData = {
            membershipNumber: membershipNumber,
            loyaltyPartnerName: props.loyaltyProgram.loyaltyProgramName
        }
        validateMembership(membershipData)
    };

    const validateMembership = (data) => {
        loyaltyProgramService.validateMembership(data).then((res) => {
            if(res){
                props.onSetMembership(res);
                props.onChangeModalState("input");
            } else {
                setMembershipValidationError(true)
            }
        }).catch(e => {
            setMembershipValidationError(true)
        })
    }

    return (
        <>
            <GiftOutlined style={{ fontSize: "60px" }} />
            <h1>Transfer Your Miles</h1>
            <h4>Link your {props.loyaltyProgram.loyaltyProgramName} account to start</h4>
            <p>
                Once linked, we will use this membership for your future miles
                transfers
            </p>
            <Form
                name="membershipForm"
                layout="vertical"
                initialValues={{ remember: true }}
                onFinish={onFinish}
                onFinishFailed={onFinishFailed}
            >
                <Form.Item
                    label="Primary Cardholder"
                    name="name"
                    rules={[
                        {
                            required: true,
                            message: "Please input your Membership name!",
                        },
                    ]}
                >
                    <Input defaultValue={props.user.firstName + " " + props.user.lastName} />
                </Form.Item>

                <Form.Item
                    label="Membership #"
                    name="membershipNumber"
                    rules={[
                        {
                            required: true,
                            message: "Please input your membership number!",
                        },
                    ]}
                >
                    <Input onChange={(e) => setMembershipNumber(e.target.value)} />
                </Form.Item>

                <Form.Item
                    label="Confirm Membership #"
                    name="confirmMembershipNumber"
                    rules={[
                        {
                            required: true,
                            message: "Please confirm your membership number!",
                        },
                    ]}
                >
                    <Input />
                </Form.Item>
                { 
                membershipValidationError &&
                <Alert
                    message="Oh no!"
                    description="Membership Number not valid"
                    style={{ marginTop: "10px", marginBottom: "20px" }}
                    type="error"
                />
                }
                <Form.Item>
                    <Button
                        type="primary"
                        htmlType="submit"
                        style={{ width: "400px" }}
                        onClick={onClickSaveMembership}
                    >
                        Save Membership
                    </Button>
                </Form.Item>
            </Form>
            <p>
                Please ensure that your Loyalty Program membership name matches
                your cardholder name or transfers may be rejected. Rewards can
                only be transferred to a Loyalty Program registered to the exact
                cardholder name on the Bank ABC account.
            </p>
        </>
    );
};

export default TransferMilesLinkModal;
