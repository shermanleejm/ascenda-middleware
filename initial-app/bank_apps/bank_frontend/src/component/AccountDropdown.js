import React from "react";
import { Menu, Dropdown, Avatar } from "antd";
import { DownOutlined, UserOutlined } from "@ant-design/icons";

const menu = (
    <Menu>
        <Menu.Item>
            <a href="#">Account</a>
        </Menu.Item>
        <Menu.Item>
            <a href="#">Transactions</a>
        </Menu.Item>
        <Menu.Divider />
        <Menu.Item>
            <a href="#">Sign out</a>
        </Menu.Item>
    </Menu>
);

const AccountDropdown = () => {
    return (
        <Dropdown overlay={menu}>
            <span
                className="ant-dropdown-link"
                style={{ cursor: "pointer" }}
                onClick={(e) => e.preventDefault()}
            >
                <Avatar size={30} icon={<UserOutlined />} style={{marginRight: "10px"}}/>
                <DownOutlined />
            </span>
        </Dropdown>
    );
};

export default AccountDropdown;
