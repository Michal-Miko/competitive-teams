import React, { useEffect, useState, useContext } from "react";
import { useQuery, useQueryClient } from "react-query";
import {
  Layout,
  Card,
  Collapse,
  Typography,
  Spin,
  AutoComplete,
  Row,
  Pagination,
  Table,
} from "antd";
import "./index.css";

import { Api } from "../../Api";
import Team from "../Team";

import { AuthContext } from "../Auth/Auth";

const { Content } = Layout;
const { Panel } = Collapse;
const { Title } = Typography;

const Teams = () => {
  let { currentToken } = useContext(AuthContext);
  let fbToken = currentToken ? currentToken : null;
  const queryClient = useQueryClient();
  const [currentPage, setCurrentPage] = useState(1);
  const [searched, setSearched] = useState("");
  const pageSize = 10;

  const { isIdle, error: err, data: teamsOnPage } = useQuery(
    ["all-teams", currentPage, searched],
    async ({ queryKey }) => {
      const [_, currentPage, searched] = queryKey;
      const res = await Api.get(
        `/teams/search/?skip=${(currentPage - 1) * pageSize}&limit=${pageSize}`,
        { headers: { "firebase-token": fbToken, name: searched } }
      );
      return res.data;
    },
    { keepPreviousData: true }
  );

  const { countIsIdle, error: countErr, data: allTeams } = useQuery(
    ["all-teams-count", searched],
    async ({ queryKey }) => {
      const [_, searched] = queryKey;
      const res = await Api.get(`/teams_count_by_search/`, {
        headers: { "firebase-token": fbToken, name: searched },
      });
      return res.data;
    }
  );

  useEffect(() => {
    setCurrentPage(1);
    queryClient.refetchQueries(["all-teams"]);
    queryClient.refetchQueries(["all-teams-count"]);
  }, [queryClient, searched, fbToken]);

  useEffect(() => {
    queryClient.refetchQueries(["all-teams"]);
  }, [queryClient, currentPage, fbToken]);

  return teamsOnPage ? (
    <Layout className="list-background">
      <Content className="site-layout-background">
        <Card>
          <Title> Teams </Title>
          <Row gutter={[0, 15]}>
            <AutoComplete
              placeholder="Search teams"
              onChange={setSearched}
              style={{ width: 200 }}
            />
          </Row>

          <Card
            bordered={false}
            bodyStyle={{
              height: "70vh",
              overflow: "auto",
            }}
          >
            <Collapse accordion>
              {teamsOnPage.map((team) => (
                <Panel header={team.name} key={team.id}>
                  <Team id={team.id} />
                </Panel>
              ))}
            </Collapse>
          </Card>

          <Row align="center" span={4}>
            <Pagination
              defaultCurrent={1}
              defaultPageSize={pageSize}
              onChange={setCurrentPage}
              total={allTeams}
              current={currentPage}
              showSizeChanger={false}
            />
          </Row>
        </Card>
      </Content>
    </Layout>
  ) : err || countErr ? (
    <Title>
      Api request failed for the list of teams.
      <br />
      {err ? err : null}
      {countErr ? countErr : null}
    </Title>
  ) : isIdle || countIsIdle ? (
    <Layout className="list-background">
      <Content className="site-layout-background">
        <Card>
          <Table></Table>
        </Card>
      </Content>
    </Layout>
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

export default Teams;
