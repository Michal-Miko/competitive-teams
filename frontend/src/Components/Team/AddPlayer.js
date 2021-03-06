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

const validateMessages = {
  // eslint-disable-next-line
  required: "${label} is required!",
};

const openNotificationWithIcon = (type, title, msg) => {
  notification[type]({
    message: title,
    description: msg,
  });
};

const AddPlayer = ({ teamid }) => {
  let { currentToken, userData } = useContext(AuthContext);
  let fbToken = currentToken ? currentToken : null;
  const hdrs = { headers: { "firebase-token": fbToken } };
  const [visible, setVisible] = useState(false);
  const [playerIDs, setPlayerIDs] = useState({});
  const [playerQueryIDs, setPlayerQueryIDs] = useState({});

  const queryClient = useQueryClient();

  const handleSearch = (value) => {
    Api.get("/players/search/", {
      headers: {
        "firebase-token": fbToken,
        name: value,
      },
    }).then((result) => {
      setPlayerIDs(
        result.data.reduce((acc, { id, name }) => {
          acc[name] = id;
          return acc;
        }, {})
      );
      setPlayerQueryIDs({
        ...playerQueryIDs,
        ...result.data.reduce((acc, { id, name }) => {
          acc[name] = id;
          return acc;
        }, {}),
      });
    });
  };

  const onFinish = (values) => {
    values.playerid = playerQueryIDs[values.player];
    Api.put("/players/" + teamid + "?player_id=" + values.playerid, {}, hdrs)
      .then(() => {
        openNotificationWithIcon(
          "success",
          "Success",
          "Player " + values.player + " has been added to the team."
        );
        queryClient.refetchQueries(["team", teamid]);
        queryClient.refetchQueries(["teams", currentToken, userData]);
        queryClient.refetchQueries(["capTeams", currentToken, userData]);
      })
      .catch((err) => {
        openNotificationWithIcon(
          "error",
          "Error when adding player to the team",
          err.response && err.response.data.detail
            ? err.response.data.detail
            : err.message
        );
      });
    setVisible(false);
  };

  const playerForm = (
    <Form
      {...layout}
      name="nest-messages"
      onFinish={onFinish}
      validateMessages={validateMessages}
    >
      <Form.Item name="player" label="Player" rules={[{ required: true }]}>
        <AutoComplete
          style={{ width: 150 }}
          onSearch={handleSearch}
          placeholder="input here"
        >
          {Object.keys(playerIDs).map((player) => (
            <Option key={player} value={player}>
              {player}
            </Option>
          ))}
        </AutoComplete>
      </Form.Item>
      <Form.Item wrapperCol={{ ...layout.wrapperCol, offset: 6 }}>
        <Space size="middle">
          <Button type="primary" htmlType="submit">
            Submit
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
        title="Add a player to the team"
        trigger="click"
        display="inline-block"
        content={playerForm}
        visible={visible}
        onVisibleChange={(v) => setVisible(v)}
        overlayStyle={{
          width: "15vw",
        }}
      >
        <Button
          type="primary"
          onClick={() => {
            setVisible(true);
          }}
        >
          Add player
        </Button>
      </Popover>
    </Col>
  );
};

export default AddPlayer;
