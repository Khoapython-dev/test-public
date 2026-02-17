package main

import (
	"encoding/json"
	"fmt"
	"log"
	"os"
)

type API struct {
	rest             map[string]interface{}
	message          map[string]interface{}
	response         map[string]interface{}
	extension_linker map[string]interface{}
}

func get_rest(part string) (map[string]interface{}, error) {
	data, err := os.ReadFile("api/" + part)
	if err != nil {
		return nil, fmt.Errorf("error reading file %s: %w", part, err)
	}
	var m map[string]interface{}
	if err := json.Unmarshal(data, &m); err != nil {
		return nil, fmt.Errorf("error parsing JSON %s: %w", part, err)
	}
	return m, nil
}

func get_message(part string) (map[string]interface{}, error) {
	data, err := os.ReadFile("api/" + part)
	if err != nil {
		return nil, fmt.Errorf("error reading file %s: %w", part, err)
	}
	var m map[string]interface{}
	if err := json.Unmarshal(data, &m); err != nil {
		return nil, fmt.Errorf("error parsing JSON %s: %w", part, err)
	}
	return m, nil
}

func get_response(part string) (map[string]interface{}, error) {
	data, err := os.ReadFile("api/" + part)
	if err != nil {
		return nil, fmt.Errorf("error reading file %s: %w", part, err)
	}
	var m map[string]interface{}
	if err := json.Unmarshal(data, &m); err != nil {
		return nil, fmt.Errorf("error parsing JSON %s: %w", part, err)
	}
	return m, nil
}

func get_extension_linker(part string) (map[string]interface{}, error) {
	data, err := os.ReadFile("api/" + part)
	if err != nil {
		return nil, fmt.Errorf("error reading file %s: %w", part, err)
	}
	var m map[string]interface{}
	if err := json.Unmarshal(data, &m); err != nil {
		return nil, fmt.Errorf("error parsing JSON %s: %w", part, err)
	}
	return m, nil
}
 func write_api(type_api string, data map[string]interface{}) error {
	if data == "rest" {
		b, err := json.MarshalIndent(data, "", "  ")
		if err != nil {
			return fmt.Errorf("error marshaling JSON: %w", err)
		}
		if err := os.WriteFile("api/rest", b, 0644); err != nil {
			return fmt.Errorf("error writing file: %w", err)
		}
	} else if data == "message" {
		b, err := json.MarshalIndent(data, "", "  ")
		if err != nil {
			return fmt.Errorf("error marshaling JSON: %w", err)
		}
		if err := os.WriteFile("api/message", b, 0644); err != nil {
			return fmt.Errorf("error writing file: %w", err)
		}
	} else if data == "response" {
		b, err := json.MarshalIndent(data, "", "  ")
		if err != nil {
			return fmt.Errorf("error marshaling JSON: %w", err)
		}
		if err := os.WriteFile("api/response", b, 0644); err != nil {
			return fmt.Errorf("error writing file: %w", err)
		}
	} else if data == "extension-linker" {
		b, err := json.MarshalIndent(data, "", "  ")
		if err != nil {
			return fmt.Errorf("error marshaling JSON: %w", err)
		}
		if err := os.WriteFile("api/extension-linker", b, 0644); err != nil {
			return fmt.Errorf("error writing file: %w", err)
		}
	} else {
		return fmt.Errorf("unknown API type: %s", type_api)
	}
	return nil
}
```

func main() {
	tests := []struct {
		name string
		fn   func(string) (map[string]interface{}, error)
	}{
		{"rest", get_rest},
		{"message", get_message},
		{"response", get_response},
		{"extension-linker", get_extension_linker},
	}

	for _, t := range tests {
		m, err := t.fn(t.name)
		if err != nil {
			log.Printf("failed to load %s: %v\n", t.name, err)
			continue
		}
		b, err := json.MarshalIndent(m, "", "  ")
		if err != nil {
			log.Printf("failed to marshal %s: %v\n", t.name, err)
			continue
		}
		fmt.Printf("=== %s ===\n%s\n", t.name, string(b))
	}
}
```