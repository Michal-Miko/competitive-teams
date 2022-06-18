import React, { useEffect, useState, useContext } from "react";
import { useQuery, useQueryClient } from "react-query";
import {
  Layout,
  Card,
  Collapse,
  Typography,
  Spin,
  Row,
  AutoComplete,
  Pagination,
} from "antd";
import "./index.css";
import { Api } from "../../Api";
import Match from "../Match";
import { AuthContext } from "../Auth/Auth";

const { Content } = Layout;
const { Panel } = Collapse;
const { Title } = Typography;
const Matches = () => {
  let { currentToken } = useContext(AuthContext);
  let fbToken = currentToken ? currentToken : null;
  const queryClient = useQueryClient();
  const [currentPage, setCurrentPage] = useState(1);
  const [searched, setSearched] = useState("");
  const pageSize = 10;

  const { isIdle, error: err, data: matchesOnPage } = useQuery(
    ["all-matches", currentPage, searched],
    async ({ queryKey }) => {
      const [_, currentPage, searched] = queryKey;
      const res = await Api.get(
        `/matches/search/?skip=${
          (currentPage - 1) * pageSize
        }&limit=${pageSize}`,
        {
          headers: { "firebase-token": fbToken, name: searched },
        }
      );
      return res.data;
    },
    { keepPreviousData: true }
  );

  const { countIsIdle, error: countErr, data: allMatches } = useQuery(
    ["all-matches-count", searched],
    async ({ queryKey }) => {
      const [_, searched] = queryKey;
      const res = await Api.get(`/matches_count_by_search/`, {
        headers: { "firebase-token": fbToken, name: searched },
      });
      return res.data;
    }
  );

  useEffect(() => {
    setCurrentPage(1);
    queryClient.refetchQueries(["all-matches"]);
    queryClient.refetchQueries(["all-matches-count"]);
  }, [queryClient, searched, fbToken]);

  useEffect(() => {
    queryClient.refetchQueries(["all-matches"]);
  }, [queryClient, currentPage, fbToken]);

  return matchesOnPage ? (
    <Layout className="list-background">
      <Content className="site-layout-background">
        <Card>
          <Title> Matches </Title>
          <Row gutter={[0, 15]}>
            <AutoComplete
              placeholder="Search matches"
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
            <Collapse>
              {matchesOnPage.map((match) => (
                <Panel header={match.name} key={match.id}>
                  <Match id={match.id} />
                </Panel>
              ))}
            </Collapse>
          </Card>
          <Row align="center">
            <Pagination
              defaultCurrent={1}
              defaultPageSize={pageSize}
              current={currentPage}
              onChange={setCurrentPage}
              total={allMatches}
              showSizeChanger={false}
            />
          </Row>
        </Card>
      </Content>
    </Layout>
  ) : err || countErr ? (
    <Title>
      Api request failed for the list of matches.
      <br />
      {err ? err : null}
      {countErr ? countErr : null}
    </Title>
  ) : isIdle || countIsIdle ? (
    <Layout>
      <Content className="site-layout-background">
        <Card></Card>
      </Content>
    </Layout>
  ) : (
    <Layout>
      <Content className="site-layout-background">
        <Card>
          <Spin />
        </Card>
      </Content>
    </Layout>
  );
};

export default Matches;
