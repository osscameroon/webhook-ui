import * as React from "react";
import {
  ChakraProvider,
  Box,
  Grid,
  theme,
  Center,
  GridItem,
  Button,
  Text,
  VStack,
  Divider,
  useColorMode,
} from "@chakra-ui/react";
import { ColorModeSwitcher } from "./ColorModeSwitcher";
import { PasswordInput } from "./components/PasswordInput";
import axios from "axios";
import { CodeBlock, solarizedLight, solarizedDark } from "react-code-blocks";

const webhookurl = "https://webhooks.osscameroon.com";

const TokenInput = ({ tokenIsSet, setTokenIsSet, setToken }: any) => {
  return (
    <>
      <Text pb={5} fontSize="md">
        Your webhook is <i color="gray.200">{webhookurl}</i>
      </Text>
      {!tokenIsSet && <PasswordInput setToken={setToken} />}
      {!tokenIsSet && (
        <Button onClick={() => setTokenIsSet(true)} isFullWidth>
          Send
        </Button>
      )}
      {tokenIsSet && (
        <Button onClick={() => setTokenIsSet(false)} isFullWidth>
          Reset token
        </Button>
      )}
    </>
  );
};

const CommandButton = ({ token, command, setOutput }: any) => {
  const onClick = React.useCallback(() => {
    setOutput("loading...");
    axios
      .get(`${webhookurl}/hooks${command}?token=${token}`)
      .then(function (response) {
        console.log(response.data)
        console.log(response)
        setOutput(response.data);
      })
      .catch(function (error) {
        setOutput(error);
      });
  }, [command, setOutput, token]);

  return (
    <Button onClick={onClick} isFullWidth>
      {command}
    </Button>
  );
};

const HookList = ({ token }: any) => {
  const [list, setList] = React.useState([]);
  const [output, setOutput] = React.useState("nothing to show :(");
  const { colorMode, toggleColorMode } = useColorMode();

  React.useEffect(() => {
    axios
      .get(`${webhookurl}/hooks/commands?token=${token}`)
      .then(function (response) {
        setList(response.data);
      })
      .catch(function (error) {
        // handle error
        console.log(error);
      });
  }, []);

  return (
    <>
      <Text pt={5}> Commands </Text>
      <Divider />
      {list.map((command, index) => (
        <CommandButton
          key={index}
          command={command}
          setOutput={setOutput}
          token={token}
        />
      ))}
      <Text pt={5}> Output </Text>
      <Divider />
      <Text maxW={["xs", "xl", "2xl", "3xl"]} textAlign="start" fontSize="md" w={["100%", "100%"]} style={{overflowX: "scroll"}}>
        <CodeBlock
          style={{ overflowX: "scroll" }}
          text={output}
          language="bash"
          showLineNumbers={true}
          startingLineNumber={1}
          theme={colorMode === "light" ? solarizedLight : solarizedDark}
        />
      </Text>
    </>
  );
};

export const App = () => {
  const [token, setToken] = React.useState("");
  const [tokenIsSet, setTokenIsSet] = React.useState(false);

  return (
    <ChakraProvider theme={theme}>
      <Box textAlign="center" fontSize="xl">
        <Grid minH="100vh" p={3}>
          <GridItem justifySelf="flex-end" rowSpan={1}>
            <ColorModeSwitcher />
          </GridItem>

          <GridItem rowSpan={tokenIsSet ? 10 : 0}>
            <Center>
              <VStack>
                <TokenInput
                  tokenIsSet={tokenIsSet}
                  setTokenIsSet={setTokenIsSet}
                  setToken={setToken}
                />
                {tokenIsSet && <HookList token={token} />}
              </VStack>
            </Center>
          </GridItem>
        </Grid>
      </Box>
    </ChakraProvider>
  );
};
