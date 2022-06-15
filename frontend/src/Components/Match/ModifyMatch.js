import React, { useContext, useState } from "react";
import {
  Popover,
  Button,
  Row,
  Col,
  Form,
  Input,
  Space,
  DatePicker,
} from "antd";
import moment from "moment";
import "./index.css";
import { AuthContext } from "../Auth/Auth";
import { Notification } from "../Util/Notification";
import { Api } from "../../Api";

const layout = {
  labelCol: { span: 8 },
  wrapperCol: { span: 16 },
};

const validateMessages = {
  // eslint-disable-next-line
  required: "${label} is required!",
};

const ModifyMatch = ({
  matchID,
  teamAName,
  teamBName,
  name,
  time,
  score1,
  score2,
}) => {
  let { currentToken } = useContext(AuthContext);
  let fbToken = currentToken ? currentToken : null;
  const hdrs = { headers: { "firebase-token": fbToken } };
  const [visible, setVisible] = useState(false);
  const [dVisible, setDVisible] = useState(false);
  const [finished, setFinished] = useState(false);

  const onFinish = (values) => {
    Api.patch(
      `/matches/${matchID}`,
      {
        name: values.name ? values.name : name,
        start_time: values.time ? values.time : time,
        finished: finished,
        score1: values.ascore ? values.ascore : score1,
        score2: values.bscore ? values.bscore : score2,
      },
      hdrs
    )
      .then(() => {
        Notification(
          "success",
          "Match " + (finished ? "resolved" : "modified") + " successfully"
        );
        setVisible(false);
        setDVisible(false);
      })
      .catch((err) =>
        Notification(
          "error",
          "Eror when " +
            (finished ? "resolving" : "modifying") +
            " match " +
            values.name,
          err.response && err.response.data.detail
            ? err.response.data.detail
            : err.message
        )
      );
    setVisible(false);
  };

  const matchDetailForm = (
    <Form
      {...layout}
      name="nest-messages"
      onFinish={onFinish}
      validateMessages={validateMessages}
      initialValues={{ name: name, time: moment(time) }}
    >
      <React.Fragment>
        <Form.Item
          name="name"
          label={`Match name`}
          rules={[{ required: true }]}
        >
          <Input />
        </Form.Item>
        <Form.Item
          name="time"
          label={`Start time`}
          rules={[{ required: true }]}
        >
          <DatePicker showTime format="YYYY-MM-DD HH:mm" />
        </Form.Item>
        <Form.Item wrapperCol={{ ...layout.wrapperCol, offset: 8 }}>
          <Space size="middle">
            <Button type="primary" htmlType="submit">
              Submit
            </Button>
            <Button type="primary" onClick={() => setDVisible(false)}>
              Cancel
            </Button>
          </Space>
        </Form.Item>
      </React.Fragment>
    </Form>
  );

  const matchResolveForm = (
    <Form
      {...layout}
      name="nest-messages"
      onFinish={onFinish}
      validateMessages={validateMessages}
    >
      <Form.Item
        name="ascore"
        label={`${teamAName} score`}
        rules={[{ required: true }]}
      >
        <Input type="number" min={0} step={1} />
      </Form.Item>
      <Form.Item
        name="bscore"
        label={`${teamBName} score`}
        rules={[{ required: true }]}
      >
        <Input type="number" min={0} step={1} />
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
      <Row gutter={4}>
        <Col>
          <Popover
            placement="top"
            title="Modify match details"
            trigger="click"
            display="inline-block"
            content={matchResolveForm}
            visible={visible}
            onVisibleChange={(v) => setVisible(v)}
            overlayStyle={{
              width: "20vw",
            }}
          >
            <Popover content="Type in the score and finish the match. This cannot be reversed!">
              <Button
                danger
                type="primary"
                onClick={() => {
                  setFinished(true);
                  setVisible(true);
                }}
              >
                Resolve
              </Button>
            </Popover>
          </Popover>
        </Col>
        <Col>
          <Popover
            placement="top"
            title="Modify match details"
            trigger="click"
            display="inline-block"
            content={matchDetailForm}
            visible={dVisible}
            onVisibleChange={(v) => setDVisible(v)}
            overlayStyle={{
              width: "20vw",
            }}
          >
            <Button
              type="primary"
              onClick={() => {
                setDVisible(true);
              }}
            >
              Modify
            </Button>
          </Popover>
        </Col>
      </Row>
    </Col>
  );
};

export default ModifyMatch;
