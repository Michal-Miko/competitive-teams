import React, { useEffect, useState } from "react";
import "./index.css";
import G6 from "@antv/g6";

function getTextWidth(text, size, font) {
  const canvas = document.createElement("canvas");
  const context = canvas.getContext("2d");
  font = font || getComputedStyle(document.body).fontFamily;
  context.font = `${size}px ${font}`;
  return context.measureText(text).width;
}

G6.registerEdge("ladder", {
  draw(cfg, group) {
    const startPoint = cfg.startPoint;
    const endPoint = cfg.endPoint;
    const shape = group.addShape("path", {
      attrs: {
        stroke: "#333",
        path: [
          ["M", startPoint.x, startPoint.y],
          ["L", endPoint.x / 3 + (2 / 3) * startPoint.x, startPoint.y], // 1/3
          ["L", endPoint.x / 3 + (2 / 3) * startPoint.x, endPoint.y], // 2/3
          ["L", endPoint.x, endPoint.y],
        ],
      },
      name: "ladder-path-shape",
    });
    return shape;
  },
});

const nodeHeight = 90;
const padding = 50;

const SEGraph = ({ tournamentData }) => {
  const [graph, setGraph] = useState(null);
  const [nodeWidth, setNodeWidth] = useState(250);

  const getNewNodeWidth = (tournamentData) => {
    let max_width = 250;
    const matches = tournamentData.matches;
    for (const match of matches) {
      const score = match.finished
        ? `${match.score1} : ${match.score2}`
        : "TBD";
      const team1 = match.team1 !== null ? match.team1.name : "TBD";
      const team2 = match.team2 !== null ? match.team2.name : "TBD";
      const label = `${team1} vs ${team2}`;
      const labelWidth = getTextWidth(label, 20) + 80;
      if (labelWidth > max_width) max_width = labelWidth;
      const desc = `${match.name}\nScore: ${score}`;
      const descWidth = getTextWidth(desc, 10) + 100;
      if (descWidth > max_width) max_width = descWidth;
    }
    return max_width;
  };

  useEffect(() => {
    const new_width = getNewNodeWidth(tournamentData);
    setNodeWidth(new_width);

    if (graph === null) {
      const newGraph = new G6.Graph({
        container: "tournament" + tournamentData.id,
        width: Math.log2(tournamentData.teams.length) * (new_width + padding),
        height: (tournamentData.teams.length / 2) * (nodeHeight + padding),
        defaultNode: {
          type: "modelRect",
          size: [new_width, nodeHeight],
          style: {
            fill: "#3f3f3f",
            stroke: "#aaa",
            radius: 3,
          },
          labelCfg: {
            style: {
              fill: "#fff",
              fontSize: 20,
            },
          },
          descriptionCfg: {
            paddingTop: 10,
          },
        },
        defaultEdge: {
          style: {
            stroke: "#666",
            lineWidth: 2,
          },
          type: "ladder",
        },
      });
      setGraph(newGraph);
    }
  }, [tournamentData, graph]);

  useEffect(() => {
    if (graph !== null) {
      let graphData = { nodes: [], edges: [] };
      let stageMatches = Math.floor(tournamentData.teams.length / 2);
      let stage = 0;
      while (stageMatches > 0) {
        // Nodes
        for (let i = 0; i < stageMatches; i++) {
          graphData.nodes.push({
            id: "node" + (graphData.nodes.length + 1),
            label: "TBD",
            description: "Stage " + (stage + 1),
            x: (nodeWidth + padding) / 2 + stage * (nodeWidth + padding),
            y:
              i * (nodeHeight + padding) * Math.pow(2, stage) +
              (Math.pow(2, stage) * (nodeHeight + padding)) / 2,
          });
        }

        stageMatches = Math.floor(stageMatches / 2);

        // Edges
        for (let i = 0; i < stageMatches; i++) {
          graphData.edges.push(
            {
              source:
                "node" +
                ((stage > 0 ? graphData.nodes.length - stageMatches * 2 : 0) +
                  (i + 1) * 2 -
                  1),
              target: "node" + (graphData.nodes.length + i + 1),
            },
            {
              source:
                "node" +
                ((stage > 0 ? graphData.nodes.length - stageMatches * 2 : 0) +
                  (i + 1) * 2),
              target: "node" + (graphData.nodes.length + i + 1),
            }
          );
        }
        stage++;
      }

      // Match data
      const sortedMatches = tournamentData.matches.sort(
        (a, b) => a.tournament_place - b.tournament_place
      );
      for (let i = 0; i < sortedMatches.length; i++) {
        const match = sortedMatches[i];
        const score = match.finished
          ? `${match.score1} : ${match.score2}`
          : "TBD";
        const team1 = match.team1 !== null ? match.team1.name : "TBD";
        const team2 = match.team2 !== null ? match.team2.name : "TBD";
        const label = `${team1} vs ${team2}`;
        const desc = `${match.name}\nScore: ${score}`;
        graphData.nodes[i].label = label;
        graphData.nodes[i].description = desc;
        if (!match.finished) graphData.nodes[i].stateIcon = { show: false };
      }
      graph.data(graphData);
      graph.clear();
      graph.render();
    }
  }, [tournamentData, nodeWidth, graph]);

  return (
    <div style={{ overflow: "auto" }}>
      <div id={"tournament" + tournamentData.id}></div>
    </div>
  );
};

export default SEGraph;
