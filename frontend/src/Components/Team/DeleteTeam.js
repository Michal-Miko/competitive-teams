import React, { useContext, useState } from "react";
import {
  Popover,
  notification,
  Button,
  Col,
  Form,
  Space,
  AutoComplete,
} from "antd";
import { useQueryClient } from "react-query";
import "./index.css";
import { AuthContext } from "../Auth/Auth";

import { Api } from "../../Api";
const { Option } = AutoComplete;

const layout = {
  labelCol: { span: 8 },
  wrapperCol: { span: 16 },
};

const openNotificationWithIcon = (type, title, msg) => {
  notification[type]({
    message: title,
    description: msg,
  });
};

const DeleteTeam = ({ teamid }) => {
  let { currentToken, userData } = useContext(AuthContext);
  let fbToken = currentToken ? currentToken : null;
  const hdrs = { headers: { "firebase-token": fbToken } };
  const [visible, setVisible] = useState(false);
  const [playerIDs, setPlayerIDs] = useState({});
  const [playerQueryIDs, setPlayerQueryIDs] = useState({});

  const queryClient = useQueryClient();

  const onFinish = (values) => {
    values.playerid = playerQueryIDs[values.player];
    Api.delete("/teams/" + teamid, {}, hdrs)
      .then(() => {
        openNotificationWithIcon(
          "success",
          "Success",
          "Team deleted successfully."
        );
        queryClient.refetchQueries(["team", teamid]);
        queryClient.refetchQueries(["teams", currentToken, userData]);
        queryClient.refetchQueries(["capTeams", currentToken, userData]);
      })
      .catch((err) => {
        openNotificationWithIcon(
          "error",
          "Error when deleting the team",
          err.response && err.response.data.detail
            ? err.response.data.detail
            : err.message
        );
      });
    setVisible(false);
  };

  const playerForm = (
    <Form {...layout} name="nest-messages" onFinish={onFinish}>
      <Form.Item wrapperCol={{ ...layout.wrapperCol, offset: 6 }}>
        <Space size="middle">
          <Button danger type="primary" htmlType="submit">
            Confirm
          </Button>
          <Button type="primary" onClick={() => setVisible(false)}>
            Cancel
          </Button>
        </Space>
      </Form.Item>
    </Form>
  );

  return (
    <Col align="center">
      <Popover
        placement="top"
        title="Are you sure you want to delete this team?"
        trigger="click"
        display="inline-block"
        content={playerForm}
        visible={visible}
      >
        <Button
          danger
          type="primary"
          onClick={() => {
            setVisible(true);
          }}
        >
          Delete Team
        </Button>
      </Popover>
    </Col>
  );
};

export default DeleteTeam;
