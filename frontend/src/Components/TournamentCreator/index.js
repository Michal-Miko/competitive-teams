import React, { useContext, useState } from "react";
import {
  Popover,
  Button,
  Col,
  Form,
  Input,
  Space,
  DatePicker,
  InputNumber,
  Select,
  AutoComplete,
} from "antd";
import "./index.css";
import { AuthContext } from "../Auth/Auth";
import { Notification } from "../Util/Notification";
import { Api } from "../../Api";
let { Option } = Select;
const layout = {
  labelCol: { span: 11 },
  wrapperCol: { span: 16 },
};
const validateMessages = {
  // eslint-disable-next-line
  required: "${label} is required!",
};
const CreateTeams = ({ fbToken, cancel, onFinish, teamCount, isSwiss }) => {
  const [nameToId, setNameToId] = useState({});
  const [currentSearch, setCurrentSearch] = useState({});

  const handleSearch = (value) => {
    Api.get("/teams/search/", {
      headers: {
        "firebase-token": fbToken,
        name: value,
      },
    }).then((result) => {
      const searchResults = result.data.reduce((acc, { id, name }) => {
        acc[name] = id;
        return acc;
      }, {});
      setCurrentSearch(searchResults);
      setNameToId({ ...nameToId, ...searchResults });
    });
  };

  const onFinishPreprocess = (values) => {
    let new_values = {};

    if (isSwiss) new_values.swiss_rounds = values.swiss_rounds;

    let ids = [];
    for (let i = 0; i < teamCount; i++) ids.push(nameToId[values[`team_${i}`]]);
    new_values.teamIDs = ids;

    return new_values;
  };

  return (
    <Form
      {...layout}
      onFinish={(values) => onFinish(onFinishPreprocess(values))}
      validateMessages={validateMessages}
    >
      {isSwiss && (
        <Form.Item name="swiss_rounds" label="Rounds:">
          <InputNumber min={1} />
        </Form.Item>
      )}
      {[...Array(teamCount)].map((_, index) => (
        <Form.Item
          key={index}
          rules={[{ required: true }]}
          name={`team_${index}`}
          label={`Team ${index + 1}`}
        >
          <AutoComplete onSearch={handleSearch} placeholder="input here">
            {Object.keys(currentSearch).map((team) => (
              <Option key={team} value={team}>
                {team}
              </Option>
            ))}
          </AutoComplete>
        </Form.Item>
      ))}
      <Form.Item>
        <Space size="middle">
          <Button type="primary" htmlType="submit">
            Submit
          </Button>
          <Button type="primary" onClick={cancel}>
            Cancel
          </Button>
        </Space>
      </Form.Item>
    </Form>
  );
};
const CreateTournament = ({ cancel, onFinish }) => {
  const [form] = Form.useForm();

  const handleStep = (value, info) => {
    const dir = info.type === "up" ? 1 : -1;
    const currentType = form.getFieldValue("tournament_type");
    switch (currentType) {
      default:
      case "round-robin":
        value = value + 1 * dir;
        break;
      case "swiss":
        if (value % 2 !== 0) {
          value = value + 1;
        }
        value = value + 2 * dir;
        break;
      case "single-elimination":
        const log = Math.log2(value);
        value = Math.pow(2, Math.floor(log) + dir);
    }
    form.setFieldsValue({
      number_of_teams: value,
    });
  };

  const handleChange = (value) => {
    const currentType = form.getFieldValue("tournament_type");
    switch (currentType) {
      case "swiss":
        if (value % 2 !== 0) value = value + 1;
        break;
      case "single-elimination":
        const log = Math.log2(value);
        value = Math.pow(2, Math.floor(log));
        break;
      default:
        break;
    }
    form.setFieldsValue({
      number_of_teams: value,
    });
  };

  return (
    <Form
      {...layout}
      name="nest-messages"
      onFinish={onFinish}
      validateMessages={validateMessages}
      form={form}
    >
      <Form.Item name="name" label="Name" rules={[{ required: true }]}>
        <Input />
      </Form.Item>
      <Form.Item name="desc" label="Description">
        <Input />
      </Form.Item>
      <Form.Item name="starttime" label="Date">
        <DatePicker showTime format="YYYY-MM-DD HH:mm" />
      </Form.Item>
      <Form.Item
        name="tournament_type"
        label="Type:"
        rules={[{ required: true }]}
      >
        <Select>
          <Option value="round-robin">round-robin</Option>
          <Option value="swiss">swiss</Option>
          <Option value="single-elimination"> single-elimination</Option>
        </Select>
      </Form.Item>
      <Form.Item
        name="number_of_teams"
        label="Number of teams: "
        rules={[{ required: true }]}
      >
        <InputNumber
          min={2}
          step={0}
          onStep={handleStep}
          onChange={handleChange}
        />
      </Form.Item>
      <Form.Item wrapperCol={{ ...layout.wrapperCol, offset: 8 }}>
        <Space size="middle">
          <Button type="primary" htmlType="submit">
            Submit
          </Button>
          <Button type="primary" onClick={cancel}>
            Cancel
          </Button>
        </Space>
      </Form.Item>
    </Form>
  );
};

const TournamentCreator = () => {
  const { currentToken } = useContext(AuthContext);
  let fbToken = currentToken ? currentToken : null;
  const [visible, setVisible] = useState(false);
  const [tournamentInfo, setTournamentInfo] = useState({});
  const [currentForm, setCurrentForm] = useState(1);
  const [isSwiss, setIsSwiss] = useState(false);
  const cancel = () => {
    setCurrentForm(1);
    setVisible(false);
    setIsSwiss(false);
  };
  const onFinishTournamentForm = (values) => {
    setTournamentInfo(values);
    setCurrentForm(2);
    setIsSwiss(values.tournament_type === "swiss");
  };
  const onFinishTeamsForm = (values) => {
    setIsSwiss(false);
    Api.post(
      "/tournaments/",
      {
        name: tournamentInfo.name,
        description: tournamentInfo.desc,
        color: "ffffff",
        tournament_type: tournamentInfo.tournament_type,
        start_time: tournamentInfo.starttime,
        teams_ids: values.teamIDs,
        swiss_rounds: values.swiss_rounds,
      },
      {
        headers: {
          "firebase-token": fbToken,
        },
      }
    )
      .then(() => {
        setTournamentInfo({});
        Notification(
          "success",
          "Success",
          `Tournament ${tournamentInfo.name} created successfully.`
        );
      })
      .catch((err) => {
        setTournamentInfo({});
        Notification(
          "error",
          `Eror when creating tournament  + ${
            (values.name,
            err.response && err.response.data.detail
              ? err.response.data.detail
              : err.message)
          }`
        );
      });
    setVisible(false);
    setCurrentForm(1);
  };
  return (
    <Col align="center">
      <Popover
        title="Create a new tournament"
        overlayStyle={{
          width: "20vw",
          minWidth: 500,
        }}
        placement="right"
        display="inline-block"
        visible={visible}
        trigger="click"
        onVisibleChange={(v) => setVisible(v)}
        content={
          currentForm === 1 ? (
            <CreateTournament
              cancel={cancel}
              onFinish={onFinishTournamentForm}
            />
          ) : (
            <CreateTeams
              cancel={cancel}
              onFinish={onFinishTeamsForm}
              teamCount={tournamentInfo.number_of_teams}
              fbToken={fbToken}
              isSwiss={isSwiss}
            />
          )
        }
      >
        <Button className="TournamentCreator" onClick={() => setVisible(true)}>
          Create a tournament
        </Button>
      </Popover>
    </Col>
  );
};
export default TournamentCreator;
