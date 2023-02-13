import { connect } from "react-redux";
import { useEffect } from "react";
import { setAuthedUser } from "../actions/authedUser";
import { useState } from "react";
import users from "../reducers/users";
import { withRouter } from "../utils/helpers";
import { showLoading, hideLoading } from "react-redux-loading-bar";
import { Link } from "react-router-dom";
import { createUser } from "../actions/users";
import DefaultAvatar from "../images/DefaultAvatar.png";
import { MdOutlineVisibility, MdOutlineVisibilityOff } from "react-icons/md";
import { AiOutlineCheckCircle } from "react-icons/ai";
import { RxCross2 } from "react-icons/rx";
import PasswordInput from "./PasswordInput";

const CreateUser = (props) => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [avatarURL, setAvatarURL] = useState("");
  const [name, setName] = useState("");
  const [availableUserName, setAvailableUserName] = useState(true);

  const handleChangeUsername = (e) => {
    e.preventDefault();
    const newUsername = e.target.value;
    setUsername(newUsername);
    if (props.users[newUsername]) {
      setAvailableUserName(false);
    } else {
      setAvailableUserName(true);
    }
  };
  const handleChangePassword = (e) => {
    e.preventDefault();
    setPassword(e.target.value);
  };
  const handleChangeAvatarURL = (e) => {
    e.preventDefault();
    setAvatarURL(e.target.value);
  };
  const handleChangeName = (e) => {
    e.preventDefault();
    setName(e.target.value);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    // If the username does not exist, return.
    if (props.users[username]) {
      setAvailableUserName(false);
      return;
    }
    props.dispatch(createUser(username, password, name, avatarURL));
    props.dispatch(setAuthedUser(username));
    props.router.navigate("/");
    return;
  };

  return (
    <div className="create-user-profile-container">
      <form onSubmit={handleSubmit}>
        <h1>Create a profile</h1>

        <p>Full Name</p>
        <input type="text" value={name} onChange={handleChangeName} />
        <p>Username</p>
        <input type="text" value={username} onChange={handleChangeUsername} />
        {availableUserName && username !== "" && (
          <i>
            <AiOutlineCheckCircle color="#72BD7A" />
          </i>
        )}
        {!availableUserName && username !== "" && (
          <i>
            <RxCross2 color="#e85a4f" />
            <span style={{ color: "#e85a4f" }}> Username taken</span>
          </i>
        )}
        <p>Password</p>
        <PasswordInput
          password={password}
          handleChangePassword={handleChangePassword}
        />
        <p>Profile Picture URL</p>
        <input type="text" value={avatarURL} onChange={handleChangeAvatarURL} />
        <p />
        <div
          className="profile-avatar"
          style={{
            backgroundImage: `url(${avatarURL ? avatarURL : DefaultAvatar})`,
            height: "100px",
            width: "100px",
          }}
        />
        <br />
        <br />
        <button
          className="btn"
          type="submit"
          disabled={username === "" || password === ""}
        >
          Submit
        </button>
      </form>
    </div>
  );
};

const mapStateToProps = ({ users }) => ({ users });

export default withRouter(connect(mapStateToProps)(CreateUser));