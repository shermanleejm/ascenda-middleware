import React from "react";
import BankRewardsOverviewComponent from "../component/BankRewardsOverviewComponent";
import TransferMilesComponent from "../component/TransferMilesComponent";

const TransferRewardsContainer = (props) => {
    return (
        <div>
            <p style={{ fontSize: "20px" }}>
                <b>{props.user.firstName}</b>, take a look at your rewards
            </p>
            <div style={{ display: "flex", justifyContent: "space-between" }}>
                <span
                    style={{
                        borderBottom: "3px solid #1170A5",
                        cursor: "pointer",
                    }}
                >
                    Overview
                </span>
                <div>
                    <a href="#" style={{ marginRight: "30px" }}>
                        Rewards History
                    </a>
                    <a href="#" style={{ marginRight: "30px" }}>
                        FAQ
                    </a>
                    <a href="#" style={{ marginRight: "10px" }}>
                        Terms and Conditions
                    </a>
                </div>
            </div>
            <div style={{ margin: "30px 0px" }}>
                <BankRewardsOverviewComponent
                    pointBalance={props.user.pointBalance}
                />
            </div>
            <hr />
            <div style={{ margin: "25px 0px" }}>
                <span>
                    Use your{" "}
                    <b>
                        {Number(props.user.pointBalance).toLocaleString()} miles
                    </b>{" "}
                    for the things that matter the most
                </span>
            </div>
            <TransferMilesComponent />
        </div>
    );
};

export default TransferRewardsContainer;
