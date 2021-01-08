import React from "react";
import { Card, Typography } from "antd";
import styles from "./BankRewardsOverviewComponent.module.css";

const { Title } = Typography;

const BankRewardsOverviewComponent = (props) => {
    return (
        <div className={styles.overviewContainer}>
            <Card className={styles.bankRewardsCard}>
                <h1 className={styles.bankRewardsTitle}>Bank ABC Rewards</h1>
            </Card>
            <div className={styles.availableMiles}>
                <Title style={{ marginBottom: "0px", fontSize: "70px" }}>
                    {Number(props.pointBalance).toLocaleString()}
                </Title>
                <span>AVAILABLE MILES</span>
            </div>
        </div>
    );
};

export default BankRewardsOverviewComponent;
