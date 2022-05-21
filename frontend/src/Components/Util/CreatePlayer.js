import { Api } from "../../Api";

export function CreatePlayer(user) {
  if (user) {
    let user_uid = getUserToken(user);
    Api.post("/players/", {
      name: user_uid.substr(0, 5),
      description: user_uid.substr(5),
      firebase_id: user_uid,
    });
  }
}
