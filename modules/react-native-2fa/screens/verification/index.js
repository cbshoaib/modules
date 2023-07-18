import React, { Fragment, useState } from "react";
import { StyleSheet, Text, TouchableOpacity, View } from "react-native";
import { useRoute } from "@react-navigation/native";
import { unwrapResult } from "@reduxjs/toolkit";
import { useSelector, useDispatch } from "react-redux";

import Input from "../../components/Input";
import Button from "../../components/Button";
import Loader from "../../components/Loader";
import { verifyCode, sendVerification } from "../../store";

const Verification = ({ navigation }) => {
  const dispatch = useDispatch();

  // This variables gets the loading status for sendVerification code api
  const loading = useSelector(
    (state) => state?.Authentication?.sendVerification?.api?.loading
  );
  // This variables gets the loading status for code verification code api
  const verifyCodeLoading = useSelector(
    (state) => state?.Authentication?.verifyCode?.api?.loading
  );

  const isLoading = !!(
    verifyCodeLoading === "pending" || loading === "pending"
  );

  const route = useRoute();
  const { method, link } = route.params;
  const [code, setCode] = useState("");

  const handleVerification = async () => {
    // This action dispatches api for code verification. It takes verification method and code as params
    dispatch(verifyCode({ method: method, code: code }))
      .then(unwrapResult)
      .then(() => {
        navigation.navigate("Home");
      })
      .catch((err) => console.log("NOT WORKING", err));
  };

  const handleResendCode = async () => {
    // This action dispatches api to get code. It takes verification method as params
    dispatch(sendVerification({ method: method }))
      .then(unwrapResult)
      .then((res) => {
        navigation.navigate("Verification", {
          method: method,
          link: res?.link
        });
      })
      .catch((err) => console.log("NOT WORKING", err));
  };
  const handleQRCode = () => {
    navigation.navigate("GoogleAuth", {
      link: link
    });
  };

  return (
    <Fragment>
      {isLoading && <Loader />}
      <View style={styles.main}>
        <View>
          {method === "google_authenticator"
            ? (
            <Text style={styles.text}>
              Enter your 6-digits code from Google Authenticator App
            </Text>
              )
            : (
            <Text style={styles.text}>
              Verification code has been sent to your{" "}
              {method === "phone_number" ? "Phone number" : "Email"}
            </Text>
              )}
          <Input
            label="Enter Code"
            returnKeyType="next"
            value={code}
            setValue={setCode}
            autoCapitalize="none"
            placeholder="Verification code"
          />
          <View>
            <Button mode="contained" onPress={handleVerification}>
              Verify
            </Button>
          </View>
          {method !== "google_authenticator" && (
            <View style={styles.resend}>
              <Text>Did not receive a code? </Text>
              <TouchableOpacity onPress={handleResendCode}>
                <Text style={styles.textPurple}>Resend</Text>
              </TouchableOpacity>
            </View>
          )}
        </View>
        {method === "google_authenticator" && (
          <View style={styles.pt15}>
            <Button mode="contained" onPress={handleQRCode}>
              Google Authenticator QR Code
            </Button>
          </View>
        )}
      </View>
    </Fragment>
  );
};
export default Verification;

const styles = StyleSheet.create({
  main: {
    padding: 10,
    width: "100%",
    height: "100%",
    display: "flex",
    flexDirection: "column",
    alignContent: "space-between",
    justifyContent: "space-between"
  },
  text: {
    marginBottom: 5,
    marginTop: 12,
    fontWeight: "bold"
  },
  textPurple: {
    color: "#2E5984",
    fontWeight: "bold"
  },
  resend: {
    paddingTop: 7,
    display: "flex",
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "flex-end"
  },
  pt15: {
    paddingTop: 15
  }
});
