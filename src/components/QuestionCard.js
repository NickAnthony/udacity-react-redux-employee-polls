import { formatTimestamp } from "../utils/helpers";
import { useNavigate } from "react-router";
import PropTypes from "prop-types";

const QuestionCard = ({ questionId, author, timestamp }) => {
  const navigate = useNavigate();
  const handleClick = (e) => {
    e.preventDefault();
    navigate(`/questions/${questionId}`);
  };
  return (
    <div className="question-card-container">
      <div className="question-card-name">{author}</div>
      <div className="question-card-timestamp">
        {formatTimestamp(timestamp)}
      </div>
      <button className="question-card-show-btn" onClick={handleClick}>
        Show
      </button>
    </div>
  );
};

QuestionCard.propTypes = {
  optionText: PropTypes.string.isRequired,
  questionVotes: PropTypes.number.isRequired,
  totalVotes: PropTypes.number.isRequired,
  chosenByAuthedUser: PropTypes.string,
};

export default QuestionCard;
