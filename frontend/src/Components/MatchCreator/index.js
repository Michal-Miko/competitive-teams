import React, { useContext, useState } from "react";
import {
  Popover,
  Button,
  Col,
  Form,
  Input,
  Space,
  DatePicker,
  AutoComplete,
} from "antd";
import "./index.css";
import { AuthContext } from "../Auth/Auth";
import { Notification } from "../Util/Notification";
import { Api } from "../../Api";

const { TextArea } = Input;
const { Option } = AutoComplete;
const layout = {
  labelCol: { span: 8 },
  wrapperCol: { span: 16 },
};

const validateMessages = {
  // eslint-disable-next-line
  required: "${label} is required!",
};

const MatchCreator = () => {
  let { currentToken } = useContext(AuthContext);
  let fbToken = currentToken ? currentToken : null;
  const [visible, setVisible] = useState(false);
  const [teamIDs, setTeamIDs] = useState({});
  const [teamQueryIDs, setTeamQueryIDs] = useState({});

  const onFinish = (values) => {
    const hdrs = {
      headers: {
        "firebase-token": fbToken,
        "team1-id": teamQueryIDs[values.team1name],
        "team2-id": teamQueryIDs[values.team2name],
      },
    };

    Api.post(
      "/matches/",
      {
        name: values.name,
        color: "ffffff",
        start_time: values.starttime,
        finished: false,
        score1: 0,
        score2: 0,
      },
      hdrs
    )

      .then(() => {
        Notification(
          "success",
          "Success",
          `Match ${values.name} between ${values.team1name} ${values.team2name} created successfully.`
        );
      })
      .catch((err) => {
        Notification(
          "error",
          "Eror when creating team " + values.name,
          err.response && err.response.data.detail
            ? err.response.data.detail
            : err.message
        );
      });
    setVisible(false);
  };
  const handleSearch = (value) => {
    Api.get("/teams/search/", {
      headers: {
        "firebase-token": fbToken,
        name: value,
      },
    }).then((result) => {
      setTeamIDs(
        result.data.reduce((acc, { id, name }) => {
          acc[name] = id;
          return acc;
        }, {})
      );
      setTeamQueryIDs({
        ...teamQueryIDs,
        ...result.data.reduce((acc, { id, name }) => {
          acc[name] = id;
          return acc;
        }, {}),
      });
    });
  };

  const matchForm = (
    <Form
      {...layout}
      name="nest-messages"
      onFinish={onFinish}
      validateMessages={validateMessages}
    >
      <Form.Item name="name" label="Name" rules={[{ required: true }]}>
        <Input />
      </Form.Item>
      <Form.Item name="starttime" label="Date">
        <DatePicker showTime format="YYYY-MM-DD HH:mm" />
      </Form.Item>
      <Form.Item
        name="team1name"
        label="Team's name"
        rules={[{ required: true }]}
      >
        <AutoComplete onSearch={handleSearch} placeholder="input here">
          {Object.keys(teamIDs).map((team) => (
            <Option key={team} value={team}>
              {team}
            </Option>
          ))}
        </AutoComplete>
      </Form.Item>
      <Form.Item
        name="team2name"
        label="Team's name"
        rules={[{ required: true }]}
      >
        <AutoComplete onSearch={handleSearch} placeholder="input here">
          {Object.keys(teamIDs).map((team) => (
            <Option key={team} value={team}>
              {team}
            </Option>
          ))}
        </AutoComplete>
      </Form.Item>
      <Form.Item wrapperCol={{ ...layout.wrapperCol, offset: 8 }}>
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
        placement="right"
        title="Create a new match"
        trigger="click"
        display="inline-block"
        content={matchForm}
        visible={visible}
        onVisibleChange={(v) => setVisible(v)}
        overlayStyle={{
          width: "20vw",
          minWidth: 500,
        }}
      >
        <Button
          className="MatchCreator"
          onClick={() => {
            setVisible(true);
          }}
        >
          Create a match
        </Button>
      </Popover>
    </Col>
  );
};

export default MatchCreator;
