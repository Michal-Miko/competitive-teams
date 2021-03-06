import React, { useContext } from "react";
import { useQuery } from "react-query";
import { Typography, Card, Table, Spin, Space, Row, Col } from "antd";
import { useParams } from "react-router-dom";
import "./index.css";

import { AuthContext } from "../Auth/Auth";
import { Api } from "../../Api";
import EditTeam from "./EditTeam";
import AddPlayer from "./AddPlayer";
import RemovePlayer from "./RemovePlayer";
import MakeCaptain from "./MakeCaptain";

const { Title } = Typography;
const { Column, ColumnGroup } = Table;
const { Meta } = Card;

const Team = ({ id, noactions }) => {
  let { currentToken, userData } = useContext(AuthContext);
  let fbToken = currentToken ? currentToken : null;

  // If no id has been passed, check router params
  const { teamid } = useParams();
  if (id === null || id === undefined) id = teamid;

  const { isIdle, error: err, data: teamData } = useQuery(
    ["team", id],
    async () => {
      const res = await Api.get("/teams/" + id, {
        headers: { "firebase-token": fbToken },
      });
      return res.data;
    },
    {
      enabled: !!id,
    }
  );

  return teamData ? (
    <div className="team-info">
      <Table
        dataSource={
          teamData.captain_id
            ? teamData.players.filter(
                (player) => player.id === teamData.captain_id
              )
            : null
        }
        size="small"
        pagination={false}
        bordered={true}
      >
        <Column
          title="Team Captain"
          dataIndex="name"
          key="capname"
          align="center"
        />
      </Table>
      <Table
        dataSource={teamData.players}
        size="small"
        pagination={false}
        bordered={true}
      >
        <ColumnGroup title="Players" align="center">
          <Column title="Name" dataIndex="name" key="playername" />
          <Column title="Bio" dataIndex="description" key="playerdesc" />
          {!noactions ? (
            <Column
              title="Actions"
              key="actions"
              render={(text, record) =>
                userData ? (
                  <Space size="small">
                    {record.id === teamData.captain_id ? null : (
                      <MakeCaptain teamid={id} playerid={record.id} />
                    )}
                    <RemovePlayer teamid={id} playerid={record.id} />
                  </Space>
                ) : null
              }
            />
          ) : null}
        </ColumnGroup>
      </Table>
      {userData && !noactions ? (
        <Card>
          <Row gutter={4} justify="center">
            <Col>
              <AddPlayer teamid={id} />
            </Col>
            <Col>
              <EditTeam teamData={teamData} />
            </Col>
          </Row>
        </Card>
      ) : null}
      <Card>
        <Meta title="About the team" description={teamData.description} />
      </Card>
    </div>
  ) : err ? (
    <Title>
      Api request failed for team with id: {id}
      <br />
      {err}
    </Title>
  ) : isIdle ? (
    <Card>
      <Table></Table>
    </Card>
  ) : (
    <Spin />
  );
};

export default Team;
