import React from 'react';
import { Button, Card } from "antd";
import { TransactionOutlined } from "@ant-design/icons"; 
import { Link } from "react-router-dom";
import styles from './TransferMilesComponent.module.css';

const TransferMilesComponent = () => {
    return (
        <Card className={styles.transferMilesCard}>
            <TransactionOutlined
                style={{ fontSize: "40px", color: "#1170A5" }}
            />
            <h1>Transfer Your Rewards</h1>
            <p>Transfer miles to rack up rewards with one of your travel Loyalty Programs</p>
            <Link to="/loyaltyprograms">
                <Button type="primary" style={{marginTop: "20px"}}>Use My Miles</Button>
            </Link>
        </Card>
    );
}

export default TransferMilesComponent;
