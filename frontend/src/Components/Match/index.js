import React, { useContext } from "react";
import { Typography, Card, Spin, Col, Row } from "antd";
import { useQuery } from "react-query";
import { useParams } from "react-router-dom";
import moment from "moment";
import "./index.css";
import { AuthContext } from "../Auth/Auth";
import { Api } from "../../Api";
import Team from "../Team";
import ModifyMatch from "./ModifyMatch";
const { Title } = Typography;

const Match = ({ id }) => {
  let { currentToken } = useContext(AuthContext);
  let fbToken = currentToken ? currentToken : null;

  // If no id has been passed, check router params
  const { matchid } = useParams();
  if (id === null || id === undefined) id = matchid;

  // Get match data
  const { isIdle, error: err, data: matchdata } = useQuery(
    ["match", id],
    async () => {
      if (id !== null && id !== undefined) {
        const res = await Api.get("/matches/" + id, {
          headers: { "firebase-token": fbToken },
        });
        return res.data;
      } else {
        throw new Error("No match id passed.");
      }
    }
  );

  function color(matchd) {
    if (matchd.finished) {
      return "#488c2d";
    }
    return "#8c8c8c";
  }
  return matchdata ? (
    <div className="match-info">
      <Card
        title={
          <Title level={2}>
            <Row>
              <Col align="left" span={8}>
                {matchdata.team1 ? matchdata.team1.name : "TBD"}
              </Col>
              <Col align="center" span={8}>
                vs
              </Col>
              <Col align="right" span={8}>
                {matchdata.team2 ? matchdata.team2.name : "TBD"}
              </Col>
            </Row>
          </Title>
        }
        style={{ borderColor: color(matchdata), borderWidth: 5 }}
      >
        <Row justify="center">
          <Card bordered={false} align="center">
            <Title level={1}>
              {matchdata.score1}:{matchdata.score2}
            </Title>
          </Card>
        </Row>
        <Row gutter={16}>
          <Col span={12}>
            <Card bordered={false}>
              <Team id={matchdata.team1_id} noactions />
            </Card>
          </Col>

          <Col span={12}>
            <Card bordered={false}>
              <Team id={matchdata.team2_id} noactions />
            </Card>
          </Col>
        </Row>
        <Row justify="center">
          <Title level={3}>
            {"Date: " +
              moment(matchdata.start_time).format(
                "dddd, Do MMM YYYY [at] hh:mm a"
              )}
          </Title>
        </Row>
      </Card>
      <Card>
        <Row gutter={4} justify="center">
          <Col>
            {matchdata.tournament_id === null && !matchdata.finished ? (
              <ModifyMatch
                matchID={matchdata.id}
                name={matchdata.name}
                time={matchdata.start_time}
                description={matchdata.description}
                score1={matchdata.score1}
                score2={matchdata.score2}
                teamAName={matchdata.team1.name}
                teamBName={matchdata.team2.name}
              />
            ) : null}
          </Col>
        </Row>
      </Card>
    </div>
  ) : err ? (
    <Title>
      Api request failed for match with id: {id}
      <br />
      {err}
    </Title>
  ) : isIdle ? (
    <Card />
  ) : (
    <Spin />
  );
};

export default Match;
