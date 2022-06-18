import React, { useContext, useState } from "react";
import { Popover, notification, Button, Input, Col, Form, Space } from "antd";
import { useQueryClient } from "react-query";
import "./index.css";
import { AuthContext } from "../Auth/Auth";

import { Api } from "../../Api";

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

const EditTeam = ({ teamData }) => {
  let { currentToken, userData } = useContext(AuthContext);
  let fbToken = currentToken ? currentToken : null;
  const hdrs = { headers: { "firebase-token": fbToken } };
  const [visible, setVisible] = useState(false);

  const queryClient = useQueryClient();

  const onFinish = (values) => {
    Api.patch(
      "/teams/" + teamData.id,
      {
        name: values.name,
        description: values.description,
      },
      hdrs
    )
      .then(() => {
        openNotificationWithIcon(
          "success",
          "Success",
          "Team updated successfully."
        );
        queryClient.refetchQueries(["team", teamData.id]);
        queryClient.refetchQueries(["teams", currentToken, userData]);
        queryClient.refetchQueries(["capTeams", currentToken, userData]);
        queryClient.refetchQueries(["all-teams"]);
      })
      .catch((err) => {
        openNotificationWithIcon(
          "error",
          "Could not edit the team",
          err.response && err.response.data.detail
            ? err.response.data.detail
            : err.message
        );
      });
    setVisible(false);
  };

  const teamForm = (
    <Form
      {...layout}
      name="nest-messages"
      onFinish={onFinish}
      validateMessages={validateMessages}
      initialValues={{ name: teamData.name, description: teamData.description }}
    >
      <Form.Item name="name" label={`Team name`} rules={[{ required: true }]}>
        <Input />
      </Form.Item>
      <Form.Item name="description" label="About the team">
        <Input />
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
        title="Edit Team"
        trigger="click"
        display="inline-block"
        content={teamForm}
        visible={visible}
        onVisibleChange={(v) => setVisible(v)}
        overlayStyle={{
          width: "20vw",
          minWidth: 500,
        }}
      >
        <Button
          type="primary"
          onClick={() => {
            setVisible(true);
          }}
        >
          Edit team
        </Button>
      </Popover>
    </Col>
  );
};

export default EditTeam;
