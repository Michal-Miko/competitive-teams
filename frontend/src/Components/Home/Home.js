import React, { useEffect, useState, useContext } from "react";
import { Layout, Card, Collapse, Typography, Spin } from "antd";
import moment from "moment";
import "./index.css";

import { Api } from "../../Api";
import Match from "../Match";

import { AuthContext } from "../Auth/Auth";

const { Content } = Layout;
const { Panel } = Collapse;
const { Title } = Typography;

const Matches = () => {
  const { currentToken } = useContext(AuthContext);
  const fbToken = currentToken ? currentToken : null;

  const [matches, setMatches] = useState(null);
  const [err, setErr] = useState(null);

  useEffect(() => {
    Api.get("/upcoming_matches/?limit=5", {
      headers: { "firebase-token": fbToken },
    })
      .then((result) => {
        setMatches(result.data);
      })
      .catch((err) => {
        setMatches(null);

        setErr(err.toString());
      });
  }, [fbToken]);

  return matches ? (
    <Layout className="list-background">
      <Content className="site-layout-background">
        <Card>
          <Title level={1} align="center">
            {" "}
            Upcoming matches{" "}
          </Title>
          <Collapse>
            {matches.map((match) => (
              <Panel
                header={
                  <Title level={3} align="center">
                    {match.name +
                      " - " +
                      moment(match.start_time).format(
                        "dddd, Do MMM YYYY [at] hh:mm a"
                      )}
                  </Title>
                }
                key={match.id}
                showArrow={false}
              >
                <Match id={match.id} />
              </Panel>
            ))}
          </Collapse>
        </Card>
      </Content>
    </Layout>
  ) : err ? (
    <Title>
      Api request failed for the list of matches.
      <br />
      {err}
    </Title>
  ) : (
    <Layout className="list-background">
      <Content className="site-layout-background">
        <Card>
          <Spin />
        </Card>
      </Content>
    </Layout>
  );
};

export default Matches;
