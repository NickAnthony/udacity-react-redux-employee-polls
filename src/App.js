import "./App.css";
import { connect } from "react-redux";
import { handleInitialData } from "./actions/shared";
import { useEffect, Fragment } from "react";
import LoadingBar from "react-redux-loading-bar";
import Dashboard from "./components/Dashboard";

function App(props) {
  // Load the initial user and question data asynchronously via useEffect
  useEffect(() => {
    props.dispatch(handleInitialData());
  }, [props]);

  return (
    <Fragment>
      <LoadingBar />
      <Dashboard />
    </Fragment>
  );
}

export default connect()(App);