import React, { useState } from "react";
import "./Search.css";
import SearchIcon from "@material-ui/icons/Search";
import MicIcon from "@material-ui/icons/Mic";
import Button from "@material-ui/core/Button";
import { useHistory } from "react-router-dom";
import { useStateValue } from "../StateProvider";
import { actionTypes } from "../reducer";

function Search({ hideButtons = false }) {
  const [{ term, zipCode }, dispatch] = useStateValue();
  const [input, setInput] = useState("");
  const [zipInput, setZipInput] = useState("");
  const history = useHistory();

  const search = (e) => {
    e.preventDefault();

    if (!input.trim() || !zipInput.trim()) {
      // Check if either search term or ZIP code is empty
      alert("Please enter both search term and ZIP code.");
      return;
    }

    console.log("button clicked", input, zipInput);

    dispatch({
      type: actionTypes.SET_SEARCH_TERM,
      term: input,
      zipCode: zipInput
    });

    history.push("/search");
  };

  const handleZipChange = (e) => {
    setZipInput(e.target.value);
  };

  return (
    <form className="search">
      <div className="search__input">
        <SearchIcon className="search__inputIcon" />
        <input value={input} onChange={(e) => setInput(e.target.value)} />
        <MicIcon />
      </div>
      <div className="search__input">
        <input
          placeholder="Enter ZIP code"
          value={zipInput}
          onChange={handleZipChange}
        />
      </div>
      {!hideButtons ? (
        <div className="search__buttons">
          <Button onClick={search} type="submit" variant="outlined">
            Restaurant Search
          </Button>
        </div>
      ) : (
        <div className="search__buttons">
          <Button
            className="search__buttonsHidden"
            onClick={search}
            type="submit"
            variant="outlined"
          >
            Restaurant Search
          </Button>
        </div>
      )}
    </form>
  );
}

export default Search;
