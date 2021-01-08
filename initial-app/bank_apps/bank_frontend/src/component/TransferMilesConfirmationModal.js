import React from 'react';
import { Result, Card } from "antd";

const TransferMilesConfirmationModal = (props) => {
    return (
        <div>
            <Result
                status="success"
                title="Success!"
                subTitle={`Your ${props.transferAmount} points are on their way to your ${props.loyaltyProgram.loyaltyProgramName} Account`}
                extra={[
                    <span>
                        We'll send you an email within 5 days when they've
                        received the transfer
                    </span>,
                    <Card style={{ background: "#F2F3F2", marginTop: "20px" }}>
                        <h2 style={{ color: "#619A6C" }}>{props.referenceNumber}</h2>
                        <span>CONFIRMATION CODE</span>
                    </Card>,
                ]}
            />
        </div>
    );
}

export default TransferMilesConfirmationModal;
