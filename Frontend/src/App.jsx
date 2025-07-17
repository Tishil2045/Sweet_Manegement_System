import React from "react"
import { BrowserRouter,Route,Routes } from "react-router-dom"
import SweetDetail from "./componenets/SweetDetail"
import Nav from "./componenets/Nav"
import AddSweet from "./componenets/AddSweet"
import PurchaseSweet from "./componenets/PurchaseSweet"
import RestockSweet from "./componenets/RestockSweet"

function App() {


  return (
    <>
    <div>
      <BrowserRouter>
        <Nav></Nav>
        <Routes>
          <Route element={<SweetDetail></SweetDetail> } path='/'></Route>
          <Route element={<AddSweet></AddSweet> } path='/sweets'></Route>
          <Route element={<PurchaseSweet></PurchaseSweet> } path='/sweets/purchase'></Route>
          <Route element={<RestockSweet></RestockSweet> } path='/sweets/restock'></Route>
        </Routes>
      </BrowserRouter>
    </div>
    </>
  )
}

export default App
