import React, { useState, useEffect } from "react";
import { ReactComponent as ReactLogo } from "./logo.svg";
import { Layout, Menu, Breadcrumb, Button, Row, Col, Popover } from "antd";
import { Switch, Route, useHistory } from "react-router-dom";
import "./App.css";
import TransferRewardsContainer from "./container/TransferRewardsContainer";
import LoyaltyProgramsContainer from "./container/LoyaltyProgramsContainer";
import AccountDropdown from "./component/AccountDropdown";
import userService from "./services/userService";
import loyaltyProgramService from "./services/loyaltyProgramService";
import bankService from "./services/bankService";

const { Header, Content, Footer } = Layout;

const outcomeCodeMap = {
    "0000": "Success",
    "0001": "Member not found",
    "0002": "Member name mismatch",
    "0003": "Member account closed",
    "0004": "Member account suspended",
    "0005": "Member ineligible for accrual",
    "0099": "Unable to process, please contact support for more information",
}

const outcomeCodeColorMap = {
    "0000": "green",
    "0001": "red",
    "0002": "red",
    "0003": "red",
    "0004": "red",
    "0005": "red",
    "0099": "red",
    "PENDING": "orange"
}

function App() {
    const history = useHistory();

    const [user, setUser] = useState();
    const [loyaltyPrograms, setLoyaltyPrograms] = useState();
    const [transaction, setTransaction] = useState();

    useEffect(() => {
        getUser();
        getLoyaltyPrograms();
        getTransactions();
    }, []);

    const getUser = () => {
        userService.fetchUser().then(userResult => {
            setUser(userResult);
        });
    };

    const getLoyaltyPrograms = () => {
        loyaltyProgramService.fetchLoyaltyPrograms().then((loyaltyProgramsResult) => {
            setLoyaltyPrograms(loyaltyProgramsResult);
        });
    };

    const getTransactions = () => {
        bankService.fetchTransactions().then((transaction) => {
            setTransaction(transaction);
        });
    };

    const notificationTitle = <span style={{
        display: "flex",
        justifyContent: "center",
    }}>Transactions Status</span>;

    const notificationContent = (
        <div>
            {transaction ? transaction.map(t => {
                return (
                    <>
                        <span><b>Transaction: {t.transactionCode}</b></span><br/>
                        <span>Status: <span style={{color: outcomeCodeColorMap[t.outcomeCode]}}>{t.outcomeCode != 'PENDING' ? outcomeCodeMap[t.outcomeCode]: "Pending"}</span></span>
                        <hr/>
                    </>
                )
            }): ''}
        </div>
    );

    return (
        <Layout className="layout">
            <Header>
                <Menu theme="dark" mode="horizontal">
                    <Row>
                        <Col span={8}>
                            <Button onClick={history.goBack}>&lt; Back</Button>
                        </Col>
                        <Col
                            span={8}
                            style={{
                                display: "flex",
                                justifyContent: "center",
                            }}
                        >
                            <ReactLogo className="logo" />
                        </Col>
                        <Col span={8} style={{ textAlign: "right" }}>
                            <Menu.Item>
                                <Popover placement="bottom" title={notificationTitle} content={notificationContent} trigger="click">
                                    <Button style={{ marginRight: "30px" }} onClick={getTransactions}>Notifications</Button>
                                </Popover>
                                <AccountDropdown />
                            </Menu.Item>
                        </Col>
                    </Row>
                </Menu>
            </Header>
            <Content style={{ padding: "0 50px" }}>
                <Breadcrumb style={{ margin: "16px 0" }}>
                    <Breadcrumb.Item>Account</Breadcrumb.Item>
                    <Breadcrumb.Item>Rewards</Breadcrumb.Item>
                    <h1>Transfer Rewards</h1>
                </Breadcrumb>
                <div className="site-layout-content">
                    <Switch>
                        <Route exact path="/">
                            {user && <TransferRewardsContainer user={user} />}
                        </Route>
                        <Route exact path="/loyaltyprograms">
                            {user && loyaltyPrograms ? <LoyaltyProgramsContainer user={user} loyaltyPrograms={loyaltyPrograms}/> : ''}
                        </Route>
                    </Switch>
                </div>
            </Content>
            <Footer style={{ textAlign: "center" }}>
                Bank ABC ©2020 Created by ITSA
            </Footer>
        </Layout>
    );
}

export default App;
