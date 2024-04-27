import React from "react";
import "./SearchPage.css";
import useRestaurantSearch from "../useRestaurantSearch";
import { useStateValue } from "../StateProvider";
import { Link } from "react-router-dom";
import Search from "../components/Search";
import { useHistory } from "react-router-dom";
import { actionTypes } from "../reducer";
import logo from "../logo.jpeg";

function SearchPage() {
  const [{ term, zipCode }, dispatch] = useStateValue();

  // LIVE API CALL
  const { data } = useRestaurantSearch(term, zipCode);
  const history = useHistory();

  console.log(term)
  const recommend = (item) => {
    // Logic for recommending the item
    console.log("Item recommended:", item.gmap_id);
    dispatch({
      type: actionTypes.SET_RECOMMENDATION,
      gmap_id: item.gmap_id,
    });
    history.push("/recommendation/" + item.name);
  };

  return (
    <div className="searchPage">
      <div className="searchPage__header">
        <Link to="/">
          <img className="searchPage__logo" src={logo} alt="" />
        </Link>
        <div className="searchPage__headerBody">
          <Search hideButtons initialInput={term} initialZip={zipCode} />
        </div>
      </div>
      {term && (
        <div className="searchPage__results">
          <p className="searchPage__resultCount">
            {data === null ? `Loading results for "${term}" near ZIP code: ${zipCode}...` : `Results for "${term}" near ZIP code: ${zipCode}`}
          </p>
          {data?.items.map((item, index) => (
            <div className="searchPage__result" key={index}>
              <div
                className="searchPage__resultTitle"
                onClick={() => recommend(item)}
              >
                <h2>{item.name}</h2>
              </div>
              <p className="searchPage__resultSnippet">{item.description}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default SearchPage;
