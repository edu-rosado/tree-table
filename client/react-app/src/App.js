import ActionBar from "./components/action_bar/ActionBar";
import TopBar from "./components/TopBar";
import DataSection from "./components/data_section/DataSection";
import "./scss/index.scss";

function App() {
  return (
    <div className="App">
      <TopBar/>
      <ActionBar/>
      <DataSection/>
    </div>
  );
}

export default App;
