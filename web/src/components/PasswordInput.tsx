import * as React from "react";
import { Input, InputGroup, InputRightElement, Button } from "@chakra-ui/react";

export const PasswordInput = ({ setToken }: any) => {
  const [show, setShow] = React.useState(false);
  const handleClick = () => setShow(!show);

  return (
    <InputGroup size="md">
      <Input
        pr="4.5rem"
        type={show ? "text" : "password"}
        placeholder="Enter token"
        onChange={(event) => {setToken(event.target.value)}}
      />
      <InputRightElement width="4.5rem">
        <Button h="1.75rem" size="sm" onClick={handleClick}>
          {show ? "Hide" : "Show"}
        </Button>
      </InputRightElement>
    </InputGroup>
  );
};
