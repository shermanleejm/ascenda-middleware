import React, { useState } from "react";
import { Modal, Form, Input, Button } from "antd";
import TransferMilesInputModal from "./TransferMilesInputModal";
import TransferMilesLinkModal from "./TransferMilesLinkModal";
import TransferMilesConfirmationModal from "./TransferMilesConfirmationModal";

const TransferMilesModal = (props) => {
    const [modalState, setModalState] = useState("link");
    const [membershipData, setMembershipData] = useState()
    const [transferAmount, setTransferAmount] = useState()
    const [referenceNumber, setReferenceNumber] = useState()

    const onChangeModalState = (state) => {
        setModalState(state);
    };

    const onSetMembership = (data) => {
        setMembershipData(data)
    }

    const onSetTransferAmount = (amount) => {
        setTransferAmount(amount)
    }

    const onSetReferenceNumber = (number) => {
        setReferenceNumber(number)
    }

    return (
        <Modal
            visible={props.visible}
            onOk={props.handleOk}
            onCancel={props.handleCancel}
            footer={null}
            style={{ textAlign: "center" }}
        >
            {modalState == "link" ? (
                <TransferMilesLinkModal
                    user={props.user}
                    loyaltyProgram={props.loyaltyProgram}
                    onChangeModalState={onChangeModalState}
                    onSetMembership={onSetMembership}
                />
            ) : modalState == "input" ? (
                <TransferMilesInputModal
                    user={props.user}
                    loyaltyProgram={props.loyaltyProgram}
                    membershipData={membershipData}
                    onChangeModalState={onChangeModalState}
                    onSetTransferAmount={onSetTransferAmount}
                    onSetReferenceNumber={onSetReferenceNumber}
                />
            ) : (
                <TransferMilesConfirmationModal
                    loyaltyProgram={props.loyaltyProgram}
                    transferAmount={transferAmount}
                    referenceNumber={referenceNumber}
                    onChangeModalState={onChangeModalState}
                />
            )}
        </Modal>
    );
};

export default TransferMilesModal;
