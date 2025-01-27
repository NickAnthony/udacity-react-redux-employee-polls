import { render, fireEvent } from "@testing-library/react";
import { createTestAppWithStoreAndRouter } from "../utils/test-utils";

describe("Question", () => {
  it("will display the vote counts by clicking either of the vote buttons.", () => {
    var component = render(
      createTestAppWithStoreAndRouter("/questions/8xf0y6ziyjabvozdd253nd")
    );
    // Verify we have 2 vote options and no answer options
    expect(component.queryByTestId("answered-option")).not.toBeInTheDocument();
    expect(component.getAllByTestId("vote-option-button").length).toEqual(2);

    // Get one of the two vote options
    const voteButton = component.getAllByTestId("vote-option-button")[0];
    fireEvent.click(voteButton);

    // Verify we have 2 vote options and no answer options
    expect(
      component.queryByTestId("vote-option-button")
    ).not.toBeInTheDocument();
    expect(component.getAllByTestId("answered-option").length).toEqual(2);
  });

  it("will match the question snapshot.", () => {
    var component = render(
      createTestAppWithStoreAndRouter("/questions/8xf0y6ziyjabvozdd253nd")
    );
    expect(component).toMatchSnapshot();
  });

  it("will throw a 404 error when the question id does not exist.", () => {
    var component = render(
      createTestAppWithStoreAndRouter("/questions/idThatDoesNotExist")
    );
    // Check that the 404 component is rendered
    expect(component.getByTestId("404-error")).toBeInTheDocument();
    // Check that other components are not rendered
    expect(
      component.queryByTestId("vote-option-button")
    ).not.toBeInTheDocument();
    expect(component.queryByTestId("answered-option")).not.toBeInTheDocument();
  });
});
