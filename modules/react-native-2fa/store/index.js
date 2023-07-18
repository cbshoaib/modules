import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import { api } from "./api";
import { Alert } from "react-native";
import { mapErrors } from "../utils";

export const sendVerification = createAsyncThunk(
  "authentication/sendverification",
  async (data) => {
    try {
      const response = await api.sendVerification(data);
      return response.data;
    } catch (error) {
      Alert.alert("Error", mapErrors(error));
      throw new Error();
    }
  }
);

export const getGoogleAuthenticatorQR = createAsyncThunk(
  "authentication/getGoogleAuthenticatorQR",
  async () => {
    try {
      const response = await api.getGoogleAuthenticatorQR();
      return response.data;
    } catch (error) {
      Alert.alert("Error", mapErrors(error));
      throw new Error();
    }
  }
);

export const verifyCode = createAsyncThunk(
  "authentication/verifyCode",
  async (data) => {
    try {
      const response = await api.verifyCode(data);
      return response.data;
    } catch (error) {
      Alert.alert("Error", mapErrors(error));
      throw new Error();
    }
  }
);

const initialState = {
  sendVerification: { api: { loading: "idle", error: null }, entities: {} },
  getGoogleAuthenticatorQR: {
    api: { loading: "idle", error: null },
    entities: {}
  },
  verifyCode: {
    api: { loading: "idle", error: null },
    entities: {}
  }
};

export const slice = createSlice({
  name: "authentication",
  initialState: initialState,
  reducers: {},
  extraReducers: {
    [sendVerification.pending]: (state) => {
      if (state.sendVerification.api.loading === "idle") {
        state.sendVerification.api.loading = "pending";
      }
    },
    [sendVerification.fulfilled]: (state, action) => {
      if (state.sendVerification.api.loading === "pending") {
        state.sendVerification.entities = action.payload;
        state.sendVerification.api.loading = "idle";
      }
    },
    [sendVerification.rejected]: (state, action) => {
      if (state.sendVerification.api.loading === "pending") {
        state.sendVerification.api.error = action.error;
        state.sendVerification.api.loading = "idle";
      }
    },
    [getGoogleAuthenticatorQR.pending]: (state) => {
      if (state.getGoogleAuthenticatorQR.api.loading === "idle") {
        state.getGoogleAuthenticatorQR.api.loading = "pending";
      }
    },
    [getGoogleAuthenticatorQR.fulfilled]: (state, action) => {
      if (state.getGoogleAuthenticatorQR.api.loading === "pending") {
        state.getGoogleAuthenticatorQR.entities = action.payload;
        state.getGoogleAuthenticatorQR.api.loading = "idle";
      }
    },
    [getGoogleAuthenticatorQR.rejected]: (state, action) => {
      if (state.getGoogleAuthenticatorQR.api.loading === "pending") {
        state.getGoogleAuthenticatorQR.api.error = action.error;
        state.getGoogleAuthenticatorQR.api.loading = "idle";
      }
    },
    [verifyCode.pending]: (state) => {
      if (state.verifyCode.api.loading === "idle") {
        state.verifyCode.api.loading = "pending";
      }
    },
    [verifyCode.fulfilled]: (state, action) => {
      if (state.verifyCode.api.loading === "pending") {
        state.verifyCode.entities = action.payload;
        state.verifyCode.api.loading = "idle";
      }
    },
    [verifyCode.rejected]: (state, action) => {
      if (state.verifyCode.api.loading === "pending") {
        state.verifyCode.api.error = action.error;
        state.verifyCode.api.loading = "idle";
      }
    }
  }
});
