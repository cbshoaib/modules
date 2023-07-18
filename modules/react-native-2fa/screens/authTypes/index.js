import React, { Fragment, useContext } from "react";
import { Text, StyleSheet, View } from "react-native";
import { useSelector, useDispatch } from "react-redux";
import { unwrapResult } from "@reduxjs/toolkit";

import Button from "../../components/Button";
import Loader from "../../components/Loader";
import { OptionsContext } from "@options";
import { getGoogleAuthenticatorQR, sendVerification } from "../../store";

const AuthTypes = ({ navigation }) => {
  // This variables gets the loading status for sendVerification code api
  const loading = useSelector(
    (state) => state?.Authentication?.sendVerification?.api?.loading
  );
  // This variables gets the loading status for getGoogleAuthenticatorQR code api
  const googleAuthenticatorLoading = useSelector(
    (state) => state?.Authentication?.getGoogleAuthenticatorQR?.api?.loading
  );

  const isLoading =
    !!(loading === "pending" || googleAuthenticatorLoading === "pending");

  const dispatch = useDispatch();

  const options = useContext(OptionsContext);

  const onHandleMethod = async (method) => {
    if (method === "google_authenticator") {
      // This action dispatches api to get google authenticator qr code link.
      dispatch(getGoogleAuthenticatorQR())
        .then(unwrapResult)
        .then((res) => {
          navigation.navigate("Verification", {
            method: method,
            link: res?.link
          });
        })
        .catch((err) => console.log("NOT WORKING", err));
    } else {
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
    }
  };

  return (
    <Fragment>
      {isLoading && <Loader />}
      <View style={styles.main}>
        <Text style={styles.text}>Verification methods</Text>
        <Text style={styles.text13}>
          Please select an option for verification from the following:
        </Text>
        <View style={options.styles.FlexRowSpaceBetween}>
          <View style={[options.styles.wp50, options.styles.p5]}>
            <Button onPress={() => onHandleMethod("phone_number")}>SMS</Button>
          </View>
          <View style={[options.styles.wp50, options.styles.p5]}>
            <Button onPress={() => onHandleMethod("email")}>Email</Button>
          </View>
        </View>
        <View style={[options.styles.wp100, options.styles.p5]}>
          <Button onPress={() => onHandleMethod("google_authenticator")}>
            Google Authenticator
          </Button>
        </View>
      </View>
    </Fragment>
  );
};

const styles = StyleSheet.create({
  main: {
    padding: 10
  },
  text: {
    marginBottom: 5,
    marginTop: 12,
    fontWeight: "bold",
    fontSize: 18
  },
  text13: {
    fontSize: 13,
    marginBottom: 12
  }
});

export default AuthTypes;
