import React, { useContext } from "react";
import { notification, Button, Col } from "antd";
import { useQueryClient } from "react-query";
import "./index.css";
import { AuthContext } from "../Auth/Auth";

import { Api } from "../../Api";

const openNotificationWithIcon = (type, title, msg) => {
  notification[type]({
    message: title,
    description: msg,
  });
};

const RemovePlayer = ({ teamid, playerid }) => {
  let { currentToken, currentUser, userData } = useContext(AuthContext);
  let fbToken = currentToken ? currentToken : null;
  const hdrs = { headers: { "firebase-token": fbToken } };
  const queryClient = useQueryClient();

  const handleClick = () => {
    Api.put("/unlink_player/" + teamid + "?player_id=" + playerid, {}, hdrs)
      .then(() => {
        openNotificationWithIcon(
          "success",
          "Success",
          "Player has been removed from the team."
        );
        queryClient.refetchQueries(["team", teamid]);
        queryClient.refetchQueries(["teams", currentUser, userData]);
        queryClient.refetchQueries(["capTeams", currentUser, userData]);
      })
      .catch((err) => {
        openNotificationWithIcon(
          "error",
          "Error when removing player from the team",
          err.response && err.response.data.detail
            ? err.response.data.detail
            : err.message
        );
      });
  };

  return (
    <Col align="center">
      <Button danger type="primary" onClick={handleClick}>
        {userData.id === playerid ? "Leave" : "Remove"}
      </Button>
    </Col>
  );
};

export default RemovePlayer;
