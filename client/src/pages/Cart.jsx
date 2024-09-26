import React, { useEffect, useState } from "react";
import { HiOutlineArrowLeft } from "react-icons/hi";
import { useSelector } from "react-redux";
import { Link, Navigate } from "react-router-dom";
import CartItem from "../ui/CartItem";
import axios from "axios";
import { loadStripe } from "@stripe/stripe-js";

const Cart = () => {
  const productData = useSelector((state) => state.bazar.productData);
  const userInfo = useSelector((state) => state.bazar.userInfo);
  const [totalAmt, setTotalAmt] = useState("");

  if (!userInfo) {
    return <Navigate to="/login" />;
  }

  const stripePromise = loadStripe(import.meta.env.VITE_STRIPE_PUBLIC_KEY);

  useEffect(() => {
    const price = productData.reduce((acc, item) => acc + item.price * item.quantity, 0);
    setTotalAmt(price.toFixed(2));
  }, [productData]);

  const handleCheckout = async () => {
    const stripe = await stripePromise;
  
    try {
      const response = await axios.post("https://prueba-1-1qb5.onrender.com/api/pay", {
        items: productData, // Asegúrate de que `productData` tenga la estructura correcta
        email: userInfo.email, // Asegúrate de que `userInfo.email` esté definido
      });
  
      const checkoutSession = response.data;
  
      // Redirigir al usuario a Stripe Checkout
      const result = await stripe.redirectToCheckout({
        sessionId: checkoutSession.id,
      });
  
      if (result.error) {
        alert(result.error.message);
      }
    } catch (error) {
      console.error('Error al procesar el pago:', error);
      alert('Hubo un error al procesar el pago. Intenta de nuevo más tarde.');
    }
  };

  return (
    <div>
      <img
        className="w-full h-60 object-cover"
        src="https://images.pexels.com/photos/1435752/pexels-photo-1435752.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1"
        alt="cartImg"
      />
      {productData.length > 0 ? (
        <div className="max-w-screen-xl mx-auto py-20 flex flex-col lg:flex-row gap-10 px-4">
          <div className="w-full lg:w-2/3">
            <CartItem />
          </div>
          <div className="w-full lg:w-1/3 bg-[#fafafa] py-6 px-4">
            <div className=" flex flex-col gap-6 border-b-[1px] border-b-gray-400 pb-6">
              <h2 className="text-2xl font-medium ">Cart totals</h2>
              <p className="flex items-center gap-4 text-base">
                Subtotal{" "}
                <span className="font-titleFont font-bold text-lg">
                  ${totalAmt}
                </span>
              </p>
              <p className="flex items-start gap-4 text-base">
                Shipping{" "}
                <span>
                  Lorem, ipsum dolor sit amet consectetur adipisicing elit.
                  Quos, veritatis.
                </span>
              </p>
            </div>
            <p className="font-titleFont font-semibold flex justify-between mt-6">
              Total <span className="text-xl font-bold">${totalAmt}</span>
            </p>
            <button
              onClick={handleCheckout}
              className="text-base bg-black text-white w-full rounded-md py-3 mt-6 hover:bg-gray-800 duration-300"
            >
              proceed to checkout
            </button>
          </div>
        </div>
      ) : (
        <div className="max-w-screen-xl mx-auto py-10 flex flex-col items-center gap-2 justify-center">
          <p className="text-xl text-orange-600 font-titleFont font-semibold">
            Your Cart is Empty. Please go back to Shopping and add products to
            Cart.
          </p>
          <Link to="/">
            <button className="flex items-center gap-1 text-gray-400 hover:text-black duration-300">
              <span>
                <HiOutlineArrowLeft />
              </span>
              go shopping
            </button>
          </Link>
        </div>
      )}
    </div>
  );
};

export default Cart;
