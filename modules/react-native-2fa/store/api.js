import axios from "axios";
import { getGlobalOptions } from "@options";
import options from "../options";

const global = getGlobalOptions();
const BASE_URL = global.url;

export const sendVerification = (data) => {
  const config = {
    method: "post",
    maxBodyLength: Infinity,
    url: `${BASE_URL}/modules/two-factor-authentication/send/otp`,
    headers: {
      Authorization: `Token ${options.token}`,
      "Content-Type": "application/json"
    },
    data: data
  };
  return axios.request(config);
};

export const getGoogleAuthenticatorQR = () => {
  const config = {
    method: "get",
    maxBodyLength: Infinity,
    url: `${BASE_URL}/modules/two-factor-authentication/google/authenticator/qr`,
    headers: {
      Authorization: `Token ${options.token}`,
      "Content-Type": "application/json"
    }
  };
  return axios.request(config);
};

export const verifyCode = (data) => {
  const config = {
    method: "post",
    maxBodyLength: Infinity,
    url: `${BASE_URL}/modules/two-factor-authentication/verify/otp`,
    headers: {
      Authorization: `Token ${options.token}`,
      "Content-Type": "application/json"
    },
    data: data
  };
  return axios.request(config);
};

export const api = {
  sendVerification,
  getGoogleAuthenticatorQR,
  verifyCode
};
